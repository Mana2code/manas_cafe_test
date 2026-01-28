
pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.50.0-noble'
            args '-u root:root'
        }
    }

    environment {
        APP_REPO_URL  = 'https://github.com/Mana2code/manas_cafe.git'
        TEST_REPO_URL = 'https://github.com/Mana2code/manas_cafe_test.git'
        TEST_DIR      = 'tests_repo'
        REPORT_DIR    = 'reports'
        BASE_URL      = 'http://127.0.0.1:5001'
        FLASK_ENV     = 'testing'
        PYTHONUNBUFFERED = '1'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout Application') {
            steps {
                git url: env.APP_REPO_URL, branch: 'main'
            }
        }

        stage('Install Application Dependencies') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Initialize & Start Flask App') {
            steps {
                sh '''
                    export JENKINS_NODE_COOKIE=dontKillMe
                    export FLASK_APP=app.py
                    python -c "from app import init_db; init_db()"
                    nohup flask run --host=0.0.0.0 --port=5001 > flask.log 2>&1 &
                    echo $! > flask.pid
                    sleep 10
                '''
            }
        }

        stage('Checkout Test Repository') {
            steps {
                sh "mkdir -p ${TEST_DIR}"
                dir(env.TEST_DIR) {
                    git url: env.TEST_REPO_URL, branch: 'main'
                }
            }
        }

        stage('Install Test Dependencies') {
            steps {
                dir(env.TEST_DIR) {
                    sh '''
                        pip install -r requirements.txt
                        pip install pytest pytest-html pytest-playwright
                        playwright install chromium
                    '''
                }
            }
        }

        stage('Home Page Tests') {
            steps {
                sh "mkdir -p ${REPORT_DIR}"
                dir(env.TEST_DIR) {
                    // Targets only the home page test file
                    sh '''
                        pytest manas_cafe_test/test_home_page.py \
                          --junit-xml=../${REPORT_DIR}/home_junit.xml \
                          --html=../${REPORT_DIR}/home_report.html \
                          --self-contained-html
                    '''
                }
            }
        }

        stage('Menu Page Tests') {
            steps {
                dir(env.TEST_DIR) {
                    // Targets only the menu page test file
                    sh '''
                        pytest manas_cafe_test/test_menu_page.py \
                          --junit-xml=../${REPORT_DIR}/menu_junit.xml \
                          --html=../${REPORT_DIR}/menu_report.html \
                          --self-contained-html
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('flask.pid')) {
                    sh 'kill $(cat flask.pid) || true'
                }
            }

            // Aggregate results from both stages using wildcards
            junit allowEmptyResults: true, testResults: "${REPORT_DIR}/*_junit.xml"

            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: "${REPORT_DIR}",
                reportFiles: 'home_report.html, menu_report.html',
                reportName: 'Playwright Test Reports'
            ])
        }
    }
}
