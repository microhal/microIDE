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
        stage('Download') {
            steps {
               	sh './download.sh'
            }
        }    
    }	   
}

