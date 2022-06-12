
const api_url = "http://34.101.44.89:8000/";

// async function getUsers() {
//     const response = await fetch(api_url + "users");
//     const data = await response.json();    
//     return data;
// }

function Logout(){
    localStorage.clear();
}

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

    // const data = await response.json();
    // console.log(data);
    return response;

}

async function Register(uname,psw) {
    var response = await fetch(api_url + "register", {
        method: "POST",
        body: JSON.stringify({
            username: uname,
            name: uname,
            biography: "A user on Quotip.",
            hashed_password: psw

        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });

    // const data = await response.json();
    // console.log(data);
    return response;

}

async function TellStory(user_id,story,tag) {    

    var response = await fetch(api_url + "post/story/" + user_id + "?" + tag, {
        method: "POST",
        body: JSON.stringify({
            story_text: story,

        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });

    // const data = await response.json();
    // console.log(data);
    return response;

}

async function GetHistoryDetail(user_id,story_id) {
    var response = await fetch(api_url + "user/" + user_id + "/story/" + story_id, {
        method: "GET",
    });
    // const data = await response.json();
    // console.log(data);
    return response;

}

async function GetAllHistory(user_id) {
    var response = await fetch(api_url + "user/" + user_id + "/stories", {
        method: "GET",
    });
    // const data = await response.json();
    // console.log(data);
    return response;
}

async function GetAllTag() {
    var response = await fetch(api_url+"get/tag",{
        method:"GET",
    });

    return response;
}


