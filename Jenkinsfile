/** Desired capabilities */
def capabilities = [
  browserName: 'Firefox',
  version: '58.0',
  platform: 'Windows 10'
]

pipeline {
  agent {label 'mesos-testing'}
  options {
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  environment {
    VARIABLES = credentials('CIS_TESTS_VARIABLES')
    PYTEST_ADDOPTS =
      "--tb=short " +
      "--driver=SauceLabs " +
      "--variables=capabilities.json " +
      "--variables=${VARIABLES}"
    SAUCELABS_API_KEY = credentials('SAUCELABS_API_KEY')
  }
  stages {
    stage('Lint') {
      steps {
        sh "tox -e flake8"
      }
    }
    stage('Test') {
      steps {
        writeCapabilities(capabilities, 'capabilities.json')
        sh "tox -e py35"
      }
      post {
        always {
          archiveArtifacts 'results/*'
          junit 'results/*.xml'
          publishHTML(target: [
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'results',
            reportFiles: "py35.html",
            reportName: 'HTML Report'])
        }
      }
    }
  }
}