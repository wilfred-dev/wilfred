pipeline {
    agent { docker { image 'docker:dind' } }
    stages {
        stage('build') {
            steps {
                sh 'bash scripts/build_debian_package.sh'
            }
        }
    }
}
