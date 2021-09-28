import React, { Component } from 'react'
import ReactNotification from 'react-notifications-component'
import { store } from 'react-notifications-component';


export default class Post extends Component {
    constructor(props) {
        super(props)
        this.state = {
            url: ""
        }

        this.post_onclick = this.post_onclick.bind(this);
    }

    inputChange = e => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }

    post_onclick(e) {
        const url = this.state.url;
        const turl = url.split('/');
        const input = '/scrape?attr=' + turl.slice(-3).join('/');
        fetch(input, {
            method: "POST"
        }).then(res => {
            if (res.status == 400) {
                store.addNotification({
                    title: "Post Failed",
                    message: "nope",
                    type: "success",
                    insert: "top",
                    container: "top-right",
                    animationIn: ["animate__animated", "animate__fadeIn"],
                    animationOut: ["animate__animated", "animate__fadeOut"],
                })
            } else {
                store.addNotification({
                    title: "Post success",
                    message: "wuhu!",
                    type: "success",
                    insert: "top",
                    container: "top-right",
                    animationIn: ["animate__animated", "animate__fadeIn"],
                    animationOut: ["animate__animated", "animate__fadeOut"],
                })
            }
        })
    }

    render() {
        return (
            <div>
                <ReactNotification />
                <input name="url" placeholder="scrape web" value={this.state.url} onChange={this.inputChange}></input><br />
                <button onClick={this.post_onclick}>Post</button>
            </div>
        )
    }
}
