# State Basics

### App.jsx
```js
import './App.css'
import { useState } from 'react'

function App() {

  const [count, setCount] = useState(0)

  console.log(useState(0))

  return (
    <>
      <h2>Count: {count}</h2>
      <button onClick={() => setCount(count + 1)}>
        +
      </button>
      <button onClick={() => setCount(count - 1)}>
        -
      </button>
    </>
  )
}

export default App
```

<hr/>

### App.jsx
```js
import './App.css'
import { useState } from 'react'

function App() {

  const [isPinned, setPinned] = useState(false)

  const togglePinned = () => {
    setPinned(!isPinned)
  }

  return (
    <>
      <button onClick={togglePinned}>
        {isPinned && '📌'} Pinn This!
      </button>
    </>
  )
}

export default App
```

<hr/>


### App.jsx
```js
import './App.css'
import { useState } from 'react'

function App() {

  const [count, setCount] = useState(0)
  const [isPinned, setPinned] = useState(false)

  const togglePinned = () => {
    setPinned(p => !p)
  }

  return (
    <>
      <h2>Count: {count}</h2>
      <button onClick={() => setCount(c => c + 1)}>
        +
      </button>
      <button onClick={() => setCount(c => c - 1)}>
        -
      </button>
      <button onClick={togglePinned}>
        {isPinned && '📌'} Pinn This!
      </button>
    </>
  )
}

export default App
```

<hr/>


### App.jsx
```js
import './App.css'
import { useState } from 'react'

function App() {

  const [todos, setTodos] = useState(
    ['Learn React', 'Build a project']
  )

  const [newTodo, setNewTodo] = useState('')

  const addTodo = (newTodo) => {
    setTodos([...todos, newTodo])
    setNewTodo('')
  }
  const deleteTodo = (index) => {
    setTodos(
      todos.filter(
        (_, i) => i !== index)
    );
  }

  return (
    <>
      <h3>Todo List</h3>
      <ul>
        {todos.map((todo, index) => (
          <li key={index}>
            {todo}
            <button onClick={
              () => deleteTodo(index)}>
              Delete
            </button>
          </li>
        ))}
      </ul>
      <p>Typing: {newTodo}</p>
      <input type='text' value={newTodo}
        onChange={
          (e) => setNewTodo(e.target.value)}/>
      <button onClick={() => addTodo(newTodo)}>
        Add New Task
      </button>
    </>
  )
}

export default App
```

<hr/>
