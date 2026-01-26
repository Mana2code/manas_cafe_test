pipeline {
    agent {
        docker {
            // Using the Playwright image directly is much faster as browsers are pre-installed
            image 'mcr.microsoft.com/playwright/python:v1.50.0-noble'
            args '-u root:root'
        }
    }

    environment {
        APP_REPO_URL  = 'https://github.com/Mana2code/manas_cafe.git'
        TEST_REPO_URL = 'https://github.com/Mana2code/manas_cafe_test.git'
        TEST_DIR      = 'tests_repo'
        REPORT_DIR    = 'reports'
        // Point your tests to this URL
        BASE_URL      = 'http://0.0.0.0:5001'
    }

    stages {
        stage('Checkout App') {
            steps {
                git url: env.APP_REPO_URL, branch: 'main'
            }
        }

        stage('Install App Dependencies') {
            steps {
                sh 'pip install --upgrade pip && pip install -r requirements.txt'
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                  export JENKINS_NODE_COOKIE=dontKillMe
                  export FLASK_APP=app.py

                  # CALL YOUR FUNCTION: This handles mkdir, db.create_all(), and seeding data
                  python3 -c "from app import app, init_db; init_db()"

                  # Start Flask in the background
                  nohup flask run --host=0.0.0.0 --port=5001 > flask.log 2>&1 &
                  echo $! > flask.pid

                  # Wait for server to be ready
                  sleep 10
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
                      pip install -r requirements.txt || true
                      pip install pytest pytest-html pytest-playwright
                      # If using the playwright image, these are often already there,
                      # but ensure the specific browser is available
                      playwright install chromium
                    '''
                }
            }
        }

        stage('Run Tests') {
        steps {
            dir(env.TEST_DIR) {
                sh '''
                  mkdir -p ../${REPORT_DIR}
                  # Removed the --css flag to prevent the OSError
                  pytest --junit-xml=../${REPORT_DIR}/junit.xml \
                         --html=../${REPORT_DIR}/report.html \
                         --self-contained-html \
                         --screenshot=only-on-failure \
                         --output=../${REPORT_DIR}/test-results
                '''
            }
        }
}

    }

    post {
        always {
            sh '''
              if [ -f flask.pid ]; then
                kill $(cat flask.pid) || true
                rm flask.pid
              fi
            '''
            junit "${REPORT_DIR}/junit.xml"
            // Allows students to view the pretty HTML report in Jenkins
            publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true,
                         reportDir: "${REPORT_DIR}", reportFiles: 'report.html',
                         reportName: 'Playwright HTML Report'])
        }
    }
}
