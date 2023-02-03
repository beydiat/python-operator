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
                                name: 'DRY_RUN',
                                description: 'Lancer dry run',
                                defaultValue: false
                            )
                        ])
                    ])
                }
            }
        }
        stage('Check Params') {
            if (params.DRY_RUN){
                steps {
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
            if (params.QUALITY) {
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
        }
        stage('Build Deploy Code') {
            when {
                branch 'develop'
            }
            if (params.DEPLOY) {
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