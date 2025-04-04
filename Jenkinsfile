


pipeline {
    agent any

    options{
        // Max number of build logs to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        // Enable timestamp at each job in the pipeline
        timestamps()
    }

    environment{
        registry = 'longvudang123/garbage-detection'
        registryCredential = 'dockerhub'      
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment..'
                    dockerImage = docker.build registry + ":$BUILD_NUMBER" 
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy to Google Kubernetes Engine') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'helm' // Name of the container to be used for helm upgrade
                        image 'quandvrobusto/jenkins:lts' // The image containing helm
                    }
                }
            }
            steps {
                script {
                    container('helm') {
                        // Ensure Helm and Kubernetes are configured properly to deploy
                        sh("""
                        helm upgrade --install ocr \
                        --set image.repository=${registry} \
                        --set image.tag=${BUILD_NUMBER} \
                        ./helm/model_detection \
                        --namespace model-serving
                        """)
                    }
                }
            }
        }
    }
}