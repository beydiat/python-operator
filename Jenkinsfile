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
                    properties([
                        parameters([
                            booleanParam(
                                name: 'TEST',
                                description: 'Lancer les tests unitaires',
                                defaultValue: true
                            ),
                            booleanParam(
                                name: 'QUALITY',
                                description: 'Lancer analyse Sonar',
                                defaultValue: true
                            ),
                            booleanParam(
                                name: 'DEPLOY',
                                description: 'Déployer sur AWS',
                                defaultValue: false
                            ),
                            booleanParam(
                                name: 'DESTROY',
                                description: 'Supprimer déploiement sur AWS',
                                defaultValue: false
                            )
                        ])
                    ])
                }
            }
        }
        
        stage('Unit Testing') {
            when {
                expression { 
                   return params.TEST == true
                }
            }
            steps {
                sh """
                pytest -v --cov-report xml:coverage.xml --cov=. --junitxml=result.xml app/tests/ ias/lambda/tests
                """
            }
        }
        
        stage('Code Analysis') {
            when {
                expression { 
                   return params.QUALITY == true
                }
            }
            steps {
                sh "ls -la && pwd"
                withSonarQubeEnv(installationName: 'SONAR') { // You can override the credential to be used
                    sh """/opt/sonar-scanner/bin/sonar-scanner \
                        -Dsonar.projectKey=python-operator \
                        -Dsonar.projectName=python-operator \
                        -Dsonar.projectVersion=1.0 \
                        -Dsonar.sources=app, ias \
                        -Dsonar.exclusions=app/tests/**, ias/lambda/tests/** \
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
                   return params.DEPLOY == true
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
        stage('Destroy Ressources') {
            when {
                expression { 
                   return params.DESTROY == true
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
                terraform destroy
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