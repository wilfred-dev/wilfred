pipeline {
    agent { docker { image 'debian:latest' } }
    stages {
        stage('build') {
            steps {
                sh 'bash scripts/build_debian_package.sh'
            }
        }
    }
}
