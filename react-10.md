# Context

<code>App.jsx</code>
```js
import './App.css'
import { useState }
 from 'react'
import Child1
 from './Child1'

function App() {
  const [count, setCount]
   = useState(0)

  return (
    <div>
      <h2>App</h2>
      <Child1
        count={count} setCount={setCount} 
        />
    </div>
  )
}

export default App
```

<code>Child1.jsx</code>
```js
import Child2
 from './Child2'

function Child1(
  { count, setCount }
) {
  return (
    <div>
      <h2>Child1</h2>
      <Child2
        count={count}
        setCount={
          setCount
        } 
      />
    </div>
  )
}

export default Child1
```

<code>Child2.jsx</code>
```js
function Child2(
  { count, setCount }
) {
  return (
    <div>
      <h2>Child2</h2>
      <p>
        Count: {count}
      </p>
      <button onClick={
        () => setCount(
          count + 1
        )}>
        Increase
      </button>
    </div>
  )
}

export default Child2
```

<hr/>

<code>contexts/CountContext.jsx</code>
```js
//Before React 19
import { createContext, useState } from 'react'

const CountContext = createContext()

function CountProvider({ children }) {
  const [count, setCount] = useState(0)

  return (
    <CountContext.Provider value={{ count, setCount }}>
      {children}
    </CountContext.Provider>
  )
}

export { CountContext, CountProvider }
```
//React 19 & Later
import { createContext, useState } from 'react'

const CountContext = createContext()

function CountProvider({ children }) {
  const [count, setCount] = useState(0)

  return (
    <CountContext value={{ count, setCount }}>
      {children}
    </CountContext>
  )
}

export { CountContext, CountProvider }
```js



<code>App.jsx</code>
```js
import './App.css'
 import { CountProvider } from './contexts/CountContext'
import Child1 from './Child1'

function App() {
  return (
    <CountProvider>
      <h2>App</h2>
      <Child1 />
    </CountProvider>
  )
}

export default App
```

<code>Child1.jsx</code>
```js
import Child2 from './Child2'

function Child1() {
  return (
    <div>
      <h2>Child</h2>
      <Child2 />
    </div>
  )
}

export default Child1
```

<code>Child2.jsx</code>
```js
import { useContext } from 'react'
import { CountContext } from './contexts/CountContext'

function Child2() {
  const { count, setCount } = useContext(CountContext)

  return (
    <div>
      <h2>Child2</h2>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increase
      </button>
    </div>
  )
}

export default Child2
```

<hr/>

<code>contexts/ToggleContext.jsx</code>
```js
//Before React 19
import { createContext, useState } from 'react'

const ToggleContext = createContext()

function ToggleProvider({ children }) {
  const [isOn, setIsOn] = useState(false)

  const toggle = () => setIsOn(prev => !prev)

  return (
    <ToggleContext.Provider value={{ isOn, toggle }}>
      {children}
    </ToggleContext.Provider>
  )
}

export { ToggleContext, ToggleProvider }
```

```js
//React 19 & Later
import { createContext, useState } from 'react'

const ToggleContext = createContext()

function ToggleProvider({ children }) {
  const [isOn, setIsOn] = useState(false)

  const toggle = () => setIsOn(prev => !prev)

  return (
    <ToggleContext value={{ isOn, toggle }}>
      {children}
    </ToggleContext>
  )
}

export { ToggleContext, ToggleProvider }
```


<code>App.jsx</code>
```js
import './App.css'
import { CountProvider } from './contexts/CountContext'
import { ToggleProvider } from './contexts/ToggleContext'
import Child1 from './Child1'
import Child3 from './Child3'

function App() {
  return (
    <>
      <h2>App</h2>
      <CountProvider>
        <Child1 />
      </CountProvider>
      <ToggleProvider>
        <Child3 />
      </ToggleProvider>
    </>
  )
}

export default App
```

<code>Child3.jsx</code>
```js
import { useContext } from 'react'
import Child4 from './Child4'
import { ToggleContext } from './contexts/ToggleContext'

function Child3() {
  const { isOn } = useContext(ToggleContext)

  return (
    <div>
      <h2>Child3</h2>
      <p>Toggle {isOn ? 'On' : 'Off'}</p>
      <Child4 />
    </div>
  )
}

export default Child3
```


<code>Child4.jsx</code>
```js
import { useContext } from 'react'
import { ToggleContext } from './contexts/ToggleContext'

function Child4() {
  const { toggle } = useContext(ToggleContext)

  return (
    <div>
      <h2>Child4</h2>
      <button onClick={toggle}>Toggle</button>
    </div>
  )
}

export default Child4
```
