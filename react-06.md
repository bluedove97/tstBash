# useRef

### Counter.jsx
```js
import { useState, useRef } from 'react'

function Counter() {
  const count1 = useRef(0)
  const [count2, setCount2] = useState(0)

  const incrementRef = () => {
    count1.current += 1
    console.log('Ref Count:', count1.current)
  }
  
  return (
    <>
      <h2>Counter Counter</h2>
      <p>Count 1: {count1.current}</p>
      <p>Count 2: {count2}</p>
      <button onClick={incrementRef}>useRef</button>
      <button onClick={() => setCount2(c => c + 1)}>useState</button>
    </>
  )
}

export default Counter
```

### App.jsx
```
import './App.css'

import Counter from './Counter'

const App = () => (
  <>
    <Counter/>
  </>
)

export default App
```

<hr/>

### Counter.jsx
```js
import { useState, useRef } from 'react'

function Counter() {
  const [count1, setCount1] = useState(0)
  const [count2, setCount2] = useState(0)
  const refCount = useRef(0)

  const incrementRef = () => {
    refCount.current += 1
    console.log(
      'Ref Count:', refCount.current
    )
  }

  const syncCounts = () => {
    setCount1(refCount.current)
    setCount2(prev => prev + 1)
  }

  return (
    <>
      <h2>Counter Counter</h2>
      <p>Count 1: {count1}</p>
      <p>Count 2: {count2}</p>
      <button onClick={incrementRef}>
        useRef
      </button>
      <button onClick={syncCounts}>
        useState
      </button>
    </>
  )
}

export default Counter
```

<hr/>

### Counter.jsx
```js
import { useState } from 'react'

function Counter() {
  const [count1, setCount1] = useState(0)
  const [count2, setCount2] = useState(0)

  let countVar = 0

  const incrementVar = () => {
    countVar++
    console.log(
      'Var Count:', countVar 
    )
  }

  const syncCounts = () => {
    setCount1(countVar)
    setCount2(prev => prev + 1)
  }

  return (
    <>
      <h2>Counter App</h2>
      <p>Count 1: {count1}</p>
      <p>Count 2: {count2}</p>
      <button onClick={incrementVar}>
        local var
      </button>
      <button onClick={syncCounts}>
        useState
      </button>
    </>
  )
}

export default Counter
```


<hr/>

### Counter.jsx
```js
import { useState } from 'react'

let countVar = 0

function Counter() {
  const [count1, setCount1] = useState(0)
  const [count2, setCount2] = useState(0)

  const incrementVar = () => {
    countVar++
    console.log(
      'Var Count:', countVar 
    )
  }

  const syncCounts = () => {
    setCount1(countVar)
    setCount2(prev => prev + 1)
  }

  return (
    <>
      <h2>Counter App</h2>
      <p>Count 1: {count1}</p>
      <p>Count 2: {count2}</p>
      <button onClick={incrementVar}>
        local var
      </button>
      <button onClick={syncCounts}>
        useState
      </button>
    </>
  )
}

export default Counter
```

### App.jsx
```js
import './App.css'
import React, { useState } from 'react'

import Counter from './Counter'

const App = () => (
  <>
    <Counter/>
    <Counter/>
  </>
)

export default App
```

<hr/>

### App.jsx
```js
import './App.css'
import { useRef } from 'react'

const App = () => {
  const inputRef = useRef(null)

  const handleFocus = () => {
    console.log(inputRef.current)
    inputRef.current.focus()
  }

  return (
    <div>
      <input ref={inputRef}
      type="text" placeholder='Type...'/>
      <button onClick={handleFocus}>
        Focus Input
      </button>
    </div>
  )
}

export default App
```
