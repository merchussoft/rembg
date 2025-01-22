pipeline {
    agent any
    tools {
        maven 'Maven'
    }
	
	environment {
        SCANNER_HOME = tool 'sonarqube'
        REMBG_DISCOD = credentials('discord_rembg_channel')
    }

    stages {

        stage('check Docker info'){
            steps {
                sh 'docker compose down -v'
            }
        }


        stage('Git Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/merchussoft/rembg.git'
                echo 'Git Checkout Completed'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(credentialsId: 'sonarqube', installationName: 'sonarqube') {
                    sh '''
					$SCANNER_HOME/bin/sonar-scanner \
						-Dsonar.projectKey=rembg \
						-Dsonar.projectName=rembg \
                        -Dsonar.projectVersion=1.0 \
                        -Dsonar.sources=/var/jenkins_home/workspace/rembg \
                        -Dsonar.sourceEncoding=UTF-8
					'''
                    echo 'SonarQube Analysis Completed'
                }
            }
        }

        stage('docker compose build'){
            when {
                expression {
                    // solo se ejecuta si la etapa anterior pasa
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh 'docker compose build'
            }
        }

        stage('deploy a produccion') {
            when {
                expression {
                    // solo se ejecuta si la etapa anterior pasa
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh 'docker compose up -d'
                echo 'Application Deployed to Production'
            }
        }
    }

    post {
        success {
            sh '''
                curl -X POST -H 'Content-type: application/json' \
                -d '{"context":"✅ pipeline '${env.JOB_NAME} [${ENV.BUILD_NUMBER}]' completado con exito"}' \
                $REMBG_DISCOD    
            '''
        }
        failure {
           sh '''
                curl -X POST -H "Content-Type: application/json" \
                -d '{"content": "❌ Pipeline '${env.JOB_NAME} [${env.BUILD_NUMBER}]' falló. Revisa los logs."}' \
                $REMBG_DISCOD
            '''
        }
    }
}