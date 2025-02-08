import os
import requests
import subprocess
import zipfile
import string

flag = "HACKDAY{"
base = "http://challenges.hackday.fr:53073"
url = base + "/secure_sharing"
poss_chars = string.ascii_letters + string.punctuation + string.digits

os.makedirs("zips", exist_ok=True)
os.chdir("zips")

while True:
    for c in poss_chars:
        file_path = "../drunk_christmas_flag"
        open(file_path, "wb").write((flag + c).encode())

        with open(file_path, 'rb') as file:
            files = {'file': ('p_flag', file)}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            # print("File uploaded successfully!")

            zip_file_url = base + response.text.split('href="')[1].split('">')[0]
            # print(zip_file_url, zip_file_url.split('/')[-1])

            try:
                command = f"curl -O {zip_file_url}"
                zip_base_name = zip_file_url.split('/')[-1]
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                # print(result.stdout)

                with zipfile.ZipFile(zip_base_name, 'r') as zip_ref:
                    # List all the file names inside the zip
                    zip_file_names = zip_ref.namelist()
                    # print(f"Files in the zip: {zip_file_names}")

                    with zip_ref.open('flag.txt.enc') as file:
                        # Read the flag.txt.enc's content without extracting it from the zip
                        flag_enc = file.read()
                        # print(f"{flag_enc = }")

                    with zip_ref.open('p_flag.enc') as file:
                        # Read the p_flag.enc's content without extracting it from the zip
                        ref = file.read()
                        # print(f"{ref = }")

                if ref in flag_enc:
                    flag += c
                    print(f"{flag = }")
                    if c == "}":
                        exit()
                    else:
                        break
                else:
                    os.remove(zip_base_name)

                # if result.stderr:
                #     print("Error Output:")
                #     print(result.stderr)
                #     exit()

            except Exception as e:
                print(f"An error occurred: {e}")
                exit()
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
            exit()


# HACKDAY{Simple_Secrets_For_Weak_Cipher_1134567892}