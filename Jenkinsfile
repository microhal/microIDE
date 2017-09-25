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
        stage('Check linux download') {
            steps {
               	sh 'linux/microide_install.sh --checkDownload'
            }
        }    
    }
    post {
        always {
            deleteDir()
        }
    }
}


