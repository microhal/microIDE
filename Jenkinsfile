#!/usr/bin/env groovy

pipeline {   
    agent {
        node {
            label 'master'
        }    
    }   

    stages {
        stage('Checkout') {
            steps {
               	checkout scm          
            }
        }   
        stage('Check Linux download') {
            steps {
               	sh 'linux/microide_install.sh --checkDownload'
            }
        } 
        stage('Check Windows download') {
            steps {
               	sh 'python inst.py --verifyWindowsDownload'
            }
        }    
    }
    post {
        always {
            deleteDir()
        }
    }
}


