
const api_url = "http://127.0.0.1:8000/";

// async function getUsers() {
//     const response = await fetch(api_url + "users");
//     const data = await response.json();    
//     return data;
// }

async function getUsers() {
    const response = await fetch(api_url + "users");    
    return response;
}

async function Login(uname,psw) {
    var response = await fetch(api_url + "login", {
        method: "POST",
        body: JSON.stringify({
            username: uname,
            password: psw
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });

    const data = await response.json();
    console.log(data);

}

async function Register() {
    var response = await fetch(api_url + "register", {
        method: "POST",
        body: JSON.stringify({
            username: "haje",
            name: "haje",
            biography: "haje",
            hashed_password: "haje"

        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });

    const data = await response.json();
    console.log(data);

}

async function TellStory() {
    var response = await fetch(api_url + "user/ " + 2 + "/story", {
        method: "POST",
        body: JSON.stringify({
            story_text: "haje",

        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });

    const data = await response.json();
    console.log(data);

}

async function GetHistoryDetail() {
    var response = await fetch(api_url + "user/" + 2 + "/stories?story_detailed_id=" + 7, {
        method: "GET",
    });
    const data = await response.json();
    console.log(data);

}

async function GetAllHistory(user_id) {
    var response = await fetch(api_url + "user/" + user_id + "/stories", {
        method: "GET",
    });
    // const data = await response.json();
    // console.log(data);
    return response;
}


