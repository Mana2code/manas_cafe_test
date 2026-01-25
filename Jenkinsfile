pipeline {
    agent {
        docker {
            image 'python:3.13'
            args '-u' // unbuffered output
        }
    }

    environment {
        APP_REPO_URL  = 'https://github.com/Mana2code/manas_cafe.git'
        TEST_REPO_URL = 'https://github.com/Mana2code/manas_cafe_test.git'
        TEST_DIR      = 'tests_repo'
        REPORT_DIR    = 'reports'
    }

    stages {
        stage('Checkout App') {
            steps {
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: env.APP_REPO_URL]]])
            }
        }

        stage('Install App Dependencies') {
            steps {
                sh '''
                  python -m pip install --upgrade pip
                  if [ -f requirements.txt ]; then
                    pip install -r requirements.txt
                  fi
                  # Install browser binaries
                    playwright install chromium

                  # Install system dependencies for the browsers (requires root)
                    playwright install-deps

                '''
            }
        }

        stage('Run Flask App') {
            steps {
                // Run Flask in background
                sh '''
                  export FLASK_APP=app.py
                  export FLASK_ENV=testing
                  flask run --host=0.0.0.0 --port=5000 &
                  echo $! > flask.pid
                  # Give it a few seconds to start
                  sleep 5
                '''
            }
        }

        stage('Checkout Tests') {
            steps {
                dir(env.TEST_DIR) {
                    git url: env.TEST_REPO_URL, branch: 'main'
                }
            }
        }

        stage('Install Test Dependencies') {
            steps {
                dir(env.TEST_DIR) {
                    sh '''
                      python -m pip install --upgrade pip
                      # If tests have their own requirements
                      if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                      fi
                      # Ensure pytest is installed
                      pip install pytest
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir(env.TEST_DIR) {
                    sh '''
                      mkdir -p ../${REPORT_DIR}
                      pytest --junit-xml=../reports/junit.xml --html=../reports/report.html --self-contained-html

                    '''
                }
            }
        }
    }

    post {
        always {
            // Stop Flask app if running
            sh '''
              if [ -f flask.pid ]; then
                kill $(cat flask.pid) || true
              fi
            '''

            junit "${REPORT_DIR}/junit.xml"
        }
    }
}
