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
        
        

        stage('Build Env') {
            steps {
                sh "ls -la && pwd"
            }
        }

        stage(' Unit Testing') {
            steps {
                sh """
                pytest -v --cov-report xml:coverage.xml --cov=. --junitxml=result.xml  app/tests/
                """
            }
        }

        stage('Code Analysis') {
            steps {
                sh "ls -la && pwd"
                withSonarQubeEnv(installationName: 'SONAR') { // You can override the credential to be used
                    sh "/opt/sonar-scanner/bin/sonar-scanner \
                        -Dsonar.projectKey=python-operator \
                        -Dsonar.projectName=python-operator \
                        -Dsonar.projectVersion=1.0 \
                        -Dsonar.sources=app \
                        -Dsonar.exclusions=app/tests \
                        -Dsonar.language=py \
                        -Dsonar.sourceEncoding=UTF-8 \
                        -Dsonar.python.xunit.reportPath=result.xml  \
                        -Dsonar.python.coverage.reportPaths=coverage.xml" 
                        
                }
            }
        }

        stage('Build Deploy Code') {
            when {
                branch 'develop'
            }
            steps {
                sh """
                echo "Building Artifact"
                """

                sh """
                echo "Deploying Code"
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