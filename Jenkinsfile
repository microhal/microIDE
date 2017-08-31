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
                sh 'git submodule update --init'               
            }
        }
        stage('Download') {
            steps {
                sh ./download.sh
            }
        }
    }	
    post {
        always {
            deleteDir()
        }
    }
}
