import React, { Component } from 'react'
import ReactNotification from 'react-notifications-component'
import { store } from 'react-notifications-component';



class CRUDTable extends Component {
    constructor(props) {
        super(props)
        this.state = {
            Id: "",
            title: "",
            name: "",
            rating: "",
            review_count: ""
        }

        this.randomChange = this.randomChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onSubmit(e) {
        const dataBase = document.getElementById("databaseChoice").value;
        const Id = this.state.Id;
        const key = document.getElementById("updateItem").value;
        const value = this.state[key];
        const url = '/' + dataBase + '/id:' + Id;
        var formData = new FormData();
        formData.append(key, value);
        fetch(url, {
            method: "PUT",
            body: formData
        }).then(res => {
            console.log(res.status)
            if (res.status == 400 || res.status == 415) {
                store.addNotification({
                    title: "Put Failed",
                    message: "Nope!",
                    type: "success",
                    insert: "top",
                    container: "top-right",
                    animationIn: ["animate__animated", "animate__fadeIn"],
                    animationOut: ["animate__animated", "animate__fadeOut"],
                })
            } else {
                store.addNotification({
                    title: "Put success",
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

    inputChange = e => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }

    randomChange(e) {
        const values = document.getElementById('updateItem').value;
        this.setState({
            [values]: e.target.value
        },
            () => { console.log(this.state) }
        )
    }

    render() {
        return (
            <div>
                <ReactNotification />
                <hr />
                <p align='center'>Put</p><br />
                <div style={{ marginTop: 10 }}>
                    <h3 align="center">Update new book/author</h3>
                    <div className="form-group" align='center'>
                        <select id="databaseChoice" name="dataBase">
                            <option value="author">author</option>
                            <option value="book">book</option>
                        </select>
                    </div>
                    <div className="form-group" align='center'>
                        <label>Id:  </label>
                        <input
                            type="text"
                            name="Id"
                            value={this.state.Id}
                            onChange={this.inputChange}
                        />
                    </div>
                    <div className="form-group" align='center'>
                        <select id="updateItem">
                            <option value="title">title</option>
                            <option value="name">name</option>
                            <option value="rating">rating</option>
                            <option value="review_count">review_count</option>
                        </select>
                    </div>
                    <div className="form-group" align='center'>
                        <input
                            type="text"
                            name="random"
                            placeholder="random"
                            onChange={this.randomChange}
                        />
                    </div>
                    <div align='center'>
                        <button align='center' onClick={
                            this.onSubmit
                        }
                            className="btn btn-primary">update</button>
                    </div>
                </div>
            </div>
        )
    }
}
export default CRUDTable
