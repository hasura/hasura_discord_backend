def read_env_file(file_path):
    """Reads an .env file and returns a dictionary of environment variables."""
    env_vars = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars


def generate_gcloud_command(project, service_name, region, env_vars):
    """Generates a gcloud command for deploying a Cloud Run service with environment variables."""
    env_vars_string = ','.join([f"{key}='{value}'" for key, value in env_vars.items()])
    return f"gcloud run deploy {service_name} --project {project} --region {region} --update-env-vars {env_vars_string} --platform managed --source ."


def main():
    # Path to your .env file
    env_file_path = '.env'
    # Project, service name, and region
    project = 'hasura-bots'
    service_name = 'hasura-bots-backend'
    region = 'us-central1'

    # Read environment variables from .env file
    env_vars = read_env_file(env_file_path)

    # Generate the gcloud command
    gcloud_command = generate_gcloud_command(project, service_name, region, env_vars)

    # Print the gcloud command
    print(gcloud_command)


if __name__ == '__main__':
    main()
