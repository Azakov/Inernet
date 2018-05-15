import requests

DEFAULT = "80571890"


def main():
    id = "24885"
    get_friends(id)
    pass


def get_friends(id):
    try:
        r1 = "https://api.vk.com/method/users.get?user_ids=%s&v=5.74&access_token=" \
                  "50c73e276cb4422847490826a9e83c3c7498d11ce567fbbb131a14b964224fecf288f3962f452bddbaad1"
        r2 = requests.get(r1 % id).json()
        true_id = str(r2["response"][0]["id"])
        request = "https://api.vk.com/method/friends.get?user_id=%s&fields=nickname&v=5.74&access_token=" \
                  "50c73e276cb4422847490826a9e83c3c7498d11ce567fbbb131a14b964224fecf288f3962f452bddbaad1"
        response = requests.get(request % true_id).json()
        quantity = response["response"]["count"]
        with open("friends.txt", "w") as f:
            f.write("Количество друзей %s" % quantity)
            f.write("\n")
            for num in range(quantity):
                f.write(str(response["response"]["items"][num]["id"]))
                f.write(" ")
                f.write(str(response["response"]["items"][num]["first_name"]))
                f.write(" ")
                f.write(str(response["response"]["items"][num]["last_name"]))
                f.write("\n")

    except requests.exceptions.ReadTimeout:
        print('Oops. Read timeout occured')
    except requests.exceptions.ConnectTimeout:
        print('Oops. Connection timeout occured!')

if __name__ == '__main__':
    main()
