import React, { Component } from 'react';
import { Table } from 'reactstrap';
import './CRUD.css';
import ReactNotification from 'react-notifications-component'
import { store } from 'react-notifications-component';

class CRUD extends Component {
    constructor(props) {
        super(props)
        this.state = {
            dataBase: "",
            Id: "",
            search: "",
        }
    }

    inputChange = e => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }

    getTableHead() {
        if (!this.state.datas) return null;  //added this line
        try {
            return Object.keys(this.state.datas['0']).map((keys, index) => (
                <th className="head" key={index}>
                    {keys}
                </th>
            ))
        }
        catch (TypeError) {
            return <td>no list found</td>
        }

    }

    getTableData() {
        if (!this.state.datas) return null;  //added this line
        console.log(this.state.datas);
        return Object.keys(this.state.datas).map((row, index) => (
            <tr key={index}>
                {this.iteratedict(row)}
            </tr>
        ))
    }

    iteratedict(row) {
        if (!this.state.datas[row]) return null;
        return Object.keys(this.state.datas[row]).map((keys, index) => (
            <td key={index}> {this.state.datas[row][keys]}</td>
        )
        )
    }

    render() {
        return (
            <div>
                <ReactNotification />
                <input name="dataBase" placeholder="author/book" value={this.state.dataBase} onChange={this.inputChange}></input>
                    &nbsp;
                <input name="search" placeholder="query" value={this.state.search} onChange={this.inputChange} style={{ float: 'middle', paddingLeft: '100px' }}></input>
                <br />
                <input name="Id" placeholder="id" value={this.state.Id} onChange={this.inputChange}></input>
                    &nbsp;
                <button onClick={
                    async () => {
                        const query = this.state.search;
                        const url = '/search/' + query;
                        fetch(url, {
                            method: "GET"
                        }).then(res => res.json().then(
                            data => {
                                this.setState(
                                    { datas: data }
                                )
                            }
                        ))
                    }
                }>Search</button>
                <br />
                <button onClick={
                    async () => {
                        const id = this.state.Id;
                        const database = this.state.dataBase;
                        const url = '/' + database + '/id:' + id;
                        fetch(url, {
                            method: "GET"
                        }).then(res => res.json().then(
                            data => {
                                this.setState({ datas: data })
                            }
                        ));
                    }
                }>Get</button><br />
                <button onClick={
                    async () => {
                        const id = this.state.Id;
                        const database = this.state.dataBase;
                        const url = '/' + database + '/id:' + id;
                        fetch(url, {
                            method: "DELETE"
                        }).then(res => {
                            const code = res.status
                            console.log(code)
                            if (code == 400) {
                                store.addNotification({
                                    title: "Delete Failed",
                                    message: "nope",
                                    type: "success",
                                    insert: "top",
                                    container: "top-right",
                                    animationIn: ["animate__animated", "animate__fadeIn"],
                                    animationOut: ["animate__animated", "animate__fadeOut"],
                                })
                            } else {
                                store.addNotification({
                                    title: "delete success",
                                    message: "ooop",
                                    type: "success",
                                    insert: "top",
                                    container: "top-right",
                                    animationIn: ["animate__animated", "animate__fadeIn"],
                                    animationOut: ["animate__animated", "animate__fadeOut"],
                                })
                            }
                        });
                    }
                }>
                    delete
                    </button>
                <h1 id='title'>Book/Author Table</h1>
                <div style={{ overflowX: 'auto', overflowY: 'auto' }}>
                    <Table responsive >
                        <thead>
                            {this.getTableHead()}
                        </thead>
                        <tbody>
                            {this.getTableData()}
                        </tbody>
                    </Table>
                </div>
            </div>
        )
    }
}
export default CRUD