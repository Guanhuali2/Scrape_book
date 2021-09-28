import React, { Component } from 'react';
import { Table } from 'reactstrap';
import './CRUD.css'
import * as d3 from "d3";

class Top extends Component {
    constructor(props) {
        super(props)
        this.state = {
            dataBase: "",
            number: "",
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
                <th key={index} selected="false">
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
        return Object.keys(this.state.datas).map((row, index) => (
            <tr key={index} selected="false">
                {this.iteratedict(row)}
            </tr>
        ))
    }

    iteratedict(row) {
        if (!this.state.datas[row]) return null;
        return Object.keys(this.state.datas[row]).map((keys, index) => (
            <td key={index} selected='false'> {this.state.datas[row][keys]}</td>
        )
        )
    }

    render() {
        return (
            <div>
                <input name="dataBase" placeholder="author/book" value={this.state.dataBase} onChange={this.inputChange}></input>
                    &nbsp;
                <br></br>
                <input name="number" placeholder="number" value={this.state.number} onChange={this.inputChange}></input>
                    &nbsp;
                <button onClick={
                    async () => {
                        const query = this.state.number;
                        const datab = this.state.dataBase;
                        const url = '/' + query + '/' + datab;
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
                }>Get Top K</button>
                <br />
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
export default Top