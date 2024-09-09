import os
import subprocess


def main(dir_path):
    def get_latest_image(directory):
        files = [file for file in os.listdir(directory) if file.endswith(".jpg")]

        if not files:
            return None

        return max(files)
    
    script_path = os.path.join(os.path.dirname(__file__), 'download_s3.sh')
    subprocess.run([script_path])

    latest_image = get_latest_image(dir_path)

    return latest_image


if __name__ == '__main__':
    print(main(dir_path='./CCTVS/1'))
