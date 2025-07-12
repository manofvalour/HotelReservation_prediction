pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins...........'
                }
            }
        }
        stage('Setting up our Virtual Environment and Installing Dependencies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing Dependencies...........'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install setup.py
                    '''
                }
            }
        }

    }
}