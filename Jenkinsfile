pipeline {
    agent any 
    stages {
        stage('build') {
            steps {
                sh 'bash scripts/build_debian_package.sh'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'debian/dist/*.jar'
        }
    }
}
