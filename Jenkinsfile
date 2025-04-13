


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
        hfApiKey = credentials('hfApiKey-credential-id') 
    }

    stages {
        stage('Test') {
            steps {
                script {
                    echo 'Running tests with Docker build...'
                    sh '''
                        docker build -t test-image -f Dockerfile .
                        docker run --rm test-image bash -c "
                            cd /app/backend &&
                            pytest --cov=. --cov-report=term --cov-report=xml -v
                        "
                        docker rmi test-image
                    '''
                }
            }
        }
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
                        image 'longvudang123/custom_jelkins:lts' // The image containing helm
                    }
                }
            }
            steps {
                script {
                    container('helm') {
                        // Ensure Helm and Kubernetes are configured properly to deploy
                        sh("""
                        echo "hfApiKey is: ${hfApiKey}"
                        helm upgrade --install ocr \
                            --set image.repository=${registry} \
                            --set image.tag=${BUILD_NUMBER} \
                            --set hfApiKey="${hfApiKey}" \
                            ./helm/model_detection \
                            --namespace model-serving
                        """)
                    }
                }
            }
        }
    }
}