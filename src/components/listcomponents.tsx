"use client";
import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import { MdDelete } from "react-icons/md";

interface TodoItem {
  id: number;
  title: string;
  completed: boolean;
}

const URL = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}/api`
  : "http://localhost:3000/api";

const ListComponents = () => {
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [newTodo, setNewTodo] = useState("");
  const [todoCompleted, setTodoCompleted] = useState(false);

  // Fetch ToDo items on component mount
  useEffect(() => {
    axios
      .get(`${URL}/todos`)
      .then((response) => setTodos(response.data))
      .catch((error) => console.error(error));
  }, []);

  const addTodo = () => {
    axios
      .post<TodoItem>(`${URL}/todos`, { item: newTodo })
      .then((response) => {
        setTodos([...todos, response.data]);
        setNewTodo("");
      })
      .catch((error) => console.error(error));
  };

  const updateTodo = (id: number) => {
    axios
      .patch<TodoItem>(`${URL}/todos/${id}`, {
        item: todos.find((todo) => todo.id === id),
      })
      .then(() => {
        setTodos(
          todos.map((todo) => {
            if (todo.id === id) {
              todo.completed = !todo.completed;
              setTodoCompleted(!setTodoCompleted);
              return { ...todo };
            }
            return todo;
          })
        );
      })
      .catch((error) => console.error(error));
  };

  const deleteTodo = (id: number) => {
    axios
      .delete(`${URL}/todos/${id}`)
      .then(() => {
        setTodos(todos.filter((todo) => todo.id !== id));
      })
      .catch((error) => console.error(error));
  };

  // delete all todo items
  const deleteAllTodos = () => {
    axios
      .delete(`${URL}/todos`)
      .then(() => {
        setTodos([]);
      })
      .catch((error) => console.error(error));
  };
  return (
    <div className="space-x-2">
      <h2 className="text-6xl py-12 font-extrabold text-[#76453B] text-opacity-70">
        CRUD Operations
      </h2>
      <input
        type="text"
        value={newTodo}
        onChange={(e) => setNewTodo(e.target.value)}
        className="bg-white border-2 border-gray-200 rounded w-5/6 py-4 text-gray-700 text-lg leading-tight focus:outline-none focus:bg-white focus:border-purple-500/40"
      />
      <button
        className="bg-[#43766C] hover:ring-1 text-white text-lg font-semibold p-2 rounded"
        onClick={addTodo}
      >
        Add Item
      </button>
      <div className="flex flex-col">
        <div className=" space-y-4 py-6">
          {todos.map((todo) => (
            <div key={todo.id} className="flex space-x-6 items-center">
              <div
                className={`flex basis-10/12 bg-gradient-to-l from-slate-300/30 to-slate-100/10 border-blue-200/20 text-lg shadow-md border-2 rounded-md py-6 px-2 ${
                  todo.completed ? "line-through" : ""
                }`}
              >
                {todo.title}
              </div>

              <input
                type="checkbox"
                className="accent-emerald-500/25 h-5 w-5"
                onClick={() => {
                  updateTodo(todo.id);
                }}
              />
              <MdDelete size={30} onClick={() => deleteTodo(todo.id)} />
            </div>
          ))}
        </div>
      </div>
      <button
        className="bg-[#B19470] hover:ring-1 text-white text-lg font-semibold p-2 rounded"
        onClick={deleteAllTodos}
      >
        Delete All
      </button>
    </div>
  );
};
export default ListComponents;
