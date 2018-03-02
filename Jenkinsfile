pipeline {
    agent {
	label "devel9"
    }
    tools {
    }
    environment {
    }
    triggers {
	pollSCM("H/3 * * * *")
    }
    options {
	buildDiscarder(logRotator(artifactDaysToKeepStr: "", artifactNumToKeepStr: "", daysToKeepStr: "30", numToKeepStr: "30"))
	timestamps()
    }
    stages {
	stage("Docker") {
	    steps {
	        script {
		    def imageName = "expanding-redirector"
		    if (! env.CHANGE_BRANCH) {
			imageLabel = env.BRANCH_NAME
		    } else {
			imageLabel = env.CHANGE_BRANCH
		    }
		    if ( ! (imageLabel == "master") ) {
			println("Using branch_name ${imageLabel}")
			imageLabel = imageLabel.split(/\//)[-1].toLowerCase()
		    } else {
			println(" Using Master branch ${BRANCH_NAME}")
			imageLabel = env.BUILD_NUMBER
		    }
		    def app = docker.build("$imageName:${imageLabel}".toLowerCase(), '--pull --no-cache .')
		    if (currentBuild.resultIsBetterOrEqualTo('SUCCESS')) {
			docker.withRegistry('https://docker-os.dbc.dk', 'docker') {
			    app.push()
			    if (env.BRANCH_NAME == "master") {
				app.push "latest"
			    }
			}
		    }
		}
	    }
	}
    }
}
