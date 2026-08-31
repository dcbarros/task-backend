pipeline {

    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout') {

            steps {

                deleteDir()

                checkout scm

            }

        }


        stage('Setup') {

            steps {

                sh '''
                    python3 -m venv .venv

                    .venv/bin/python \
                        -m pip install \
                        --upgrade pip

                    .venv/bin/python \
                        -m pip install \
                        -r requirements.txt

                    mkdir -p reports
                '''

            }

        }


        stage('Unit Tests') {

            steps {

                sh '''
                    .venv/bin/python \
                        -m pytest \
                        tests/unit \
                        -v \
                        --junitxml=reports/unit.xml
                '''

            }

        }


        stage('Integration Tests') {

            steps {

                sh '''
                    .venv/bin/python \
                        -m pytest \
                        tests/integration \
                        -v \
                        --junitxml=reports/integration.xml
                '''

            }

        }

    }


    post {

        always {

            junit(
                testResults: 'reports/*.xml',
                allowEmptyResults: true
            )

        }

        success {

            echo 'Backend CI aprovada.'

        }

        failure {

            echo 'Backend CI reprovada.'

        }

    }

}