import subprocess
import venv

def create_virtualenv():
    venv_dir = 'env'
    venv.create(venv_dir, with_pip=True)
    return venv_dir

def install_packages(venv_dir):
    packages = ["flask", "pypresence"]
    subprocess.check_call([f"{venv_dir}/bin/pip", "install"] + packages)

if __name__ == "__main__":
    venv_dir = create_virtualenv()
    install_packages(venv_dir)
    print("Environment setup complete. Run the application with:")
    print(f"{venv_dir}/bin/python app.py")