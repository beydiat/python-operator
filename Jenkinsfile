pipeline {

    agent {
        node {
            label 'agent2'
        }
    }

    options {
        buildDiscarder logRotator( 
                    daysToKeepStr: '16', 
                    numToKeepStr: '10'
            )
    }

    stages {
        
        stage('Init') {
            steps {
                script {
                     sh """
                        echo "Init stage"
                    """
                    
                }
            }
        }
        
        stage('Check Params') {
            when {
                expression { 
                   return params.DRY_RUN == 'true'
                }
            }
            steps {
                script {
                    sh """
                        echo "Dry Run"
                    """
                    currentBuild.result = 'SUCCESS'
                    return
                }
            }
        }
        
        stage('Unit Testing') {
            steps {
                sh """
                pytest -v --cov-report xml:coverage.xml --cov=. --junitxml=result.xml  app/tests/
                """
            }
        }
        
        stage('Code Analysis') {
            when {
                expression { 
                   return params.QUALITY == 'true'
                }
            }
            steps {
                sh "ls -la && pwd"
                withSonarQubeEnv(installationName: 'SONAR') { // You can override the credential to be used
                    sh """/opt/sonar-scanner/bin/sonar-scanner \
                        -Dsonar.projectKey=python-operator \
                        -Dsonar.projectName=python-operator \
                        -Dsonar.projectVersion=1.0 \
                        -Dsonar.sources=app \
                        -Dsonar.exclusions=app/tests/** \
                        -Dsonar.language=py \
                        -Dsonar.sourceEncoding=UTF-8 \
                        -Dsonar.python.xunit.reportPath=result.xml  \
                        -Dsonar.python.coverage.reportPaths=coverage.xml""" 
                        
                }
            }
        }
        stage('Build Deploy Code') {
            when {
                expression { 
                   return params.DEPLOY == 'true'
                }
            }
            steps {
            
                withCredentials([string(credentialsId: 'TF_TOKEN', variable: 'SECRET')]) { //set SECRET with the credential content
                    echo "My secret text is '${SECRET}'"
                    sh"""
                    sed -i -e 's/TF_TOKEN_FOR_TF_CLOUD/${SECRET}/' ./ias/backend.tf
                    """
                }
                sh """
                echo "Building Artifact"
                cd ./ias
                terraform init
                terraform plan
                terraform apply
                """
            }
            
        }
        stage('Cleanup Workspace') {
            steps {
                cleanWs()
                sh """
                echo "Cleaned Up Workspace For Project"
                """
            }
        }

    }   
}