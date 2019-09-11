from flask import Flask, render_template, json, request, redirect
from shared.GeneralMethods import GeneralMethods
from shared.APIHelper import APIHelper
from models.HttpHeaderModel import HttpHeaderModel
from models.HttpResponseModel import HttpResponseModel
from models.AuthResponseModel import AuthResponseModel
from models.ActivityModel import ActivityModel
from models.JWTModel import JWTModel
from business.AuthManager import AuthManager
from business.UserInfoManager import UserInfoManager
from business.ActivityManager import ActivityManager
from business.JWTManager import JWTManager
import sys

app = Flask(__name__,template_folder='views')
app.secret_key = GeneralMethods.GenerateRandomString()
app.config['SESSION_TYPE'] = 'filesystem'
@app.route("/")
def main():
    config = GeneralMethods.GetConfig()

    authManager = AuthManager()
    authResponse = AuthResponseModel()
    jwt = JWTModel()

    # Authenticate (Code Exchange)
    if request.args.get('code') != None :
        # verfiy that the state parameter returned by the server is the same that was sent earlier.
        if authManager.IsValidState(request.args.get('state')) :
            authResponse = authManager.Authorize(request.args.get('code'))
            jwtManager = JWTManager(config, authResponse.id_token)
            # Decode id_token (JWT) 
            jwt = jwtManager.DecodeJWT()
            if jwtManager.ValidateJWT(jwt) :    
                authManager.SaveAuthResponse(authResponse)
            else :
                raise Exception("Invalid JWT.")
        else :
            raise Exception('State Parameter returned doesn\'t match to the one sent to Core API Server.')

    # Load Activity List
    if authManager.GetAuthResponse() != None :
        # Get the user Info
        userInfoManager = UserInfoManager()
        userInfo = userInfoManager.GetUserInfo()

        # Get Activity List
        activityManager = ActivityManager()
        activityList = activityManager.GetList()
        return render_template('ActivityListView.html', userInfo = userInfo, activityList = activityList)
    else :
        return render_template('index.html')

@app.route('/connectToCore', methods=['POST'])
def connectToCore():
    try:
        authManager = AuthManager()
        coreUrl = authManager.ConnectToCore()
        return redirect(coreUrl)
    except:
        return '<div style=\'color:red\'>' + str(sys.exc_info()[1]) + '</div>'

@app.route('/disconnectFromCore', methods=['POST'])
def disconnectFromCore():
    try:
        authManager = AuthManager()
        homeUrl = authManager.DisconnectFromCore()
        return redirect(homeUrl)
    except:
        return '<div style=\'color:red\'>' + str(sys.exc_info()[1]) + '</div>'

@app.route('/CreateActivityView')
def CreateActivityView():
    try:
        id = request.args.get('id')        
        if id != None : #update
            activityManager = ActivityManager()            
            activity = activityManager.Get(id)
            return render_template('CreateActivityView.html', activity = activity)
        else : # create  
            activity = ActivityModel('{"code":"","description":"","billable":"","costRate":"","billRate":""}')
            return render_template('CreateActivityView.html', activity = activity)
    except:
        return '<div style=\'color:red\'>' + str(sys.exc_info()[1]) + '</div>'

@app.route('/SubmitActivity', methods=['POST'])
def SubmitActivity():
    try:
        activity = ActivityModel()
        activityManager = ActivityManager()
        activity.code = request.form['code']
        activity.description = request.form['description']
        activity.billRate = request.form['billRate']
        activity.costRate = request.form['costRate']
        activity.billable = 'isBillable' in request.form

        id = request.form['id']
        if id != 'None' : #update
            activityManager.Update(id, activity)
        else : #create
            activityManager.Create(activity)
        return redirect("/")
    except:
        return '<div style=\'color:red\'>' + str(sys.exc_info()[1]) + '</div>'

@app.route('/DeleteActivity')
def DeleteActivity():
    try:
        id = request.args.get('id')
        if id != None : #update
            activityManager = ActivityManager()
            activityManager.Delete(id)
        return redirect("/")
    except:
        return '<div style=\'color:red\'>' + str(sys.exc_info()[1]) + '</div>'
    
    

if __name__ == "__main__":
    app.run()