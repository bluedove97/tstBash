# Exploring State Further

### App.css
```css
#root {
  margin: 0 auto;
}

#root button {
  margin: 4px;
  padding: 0.4em 0.8em;
  background-color: #f0f0f0;
}

input[type=text] {
  display: block;
  margin: 8px 0;
  padding: 4px;
  font-size: 0.92em;
}
```

### Profile.jsx
```js
import { useState } from 'react'

function Profile({ name }) {
  const [status, setStatus] = useState('Available')

  console.log('Profile Rendered')

  return (
    <div className="user-profile">
      <h3>Name: {name}</h3>
      <p>Status: {status}</p>
      <button onClick={() => setStatus('Away')}>
        Set Away
      </button>
      <button onClick={() => setStatus('Available')}>
        Set Available
      </button>
    </div>
  );
}

export default Profile;
```

### App.jsx
```js
import './App.css'
import { useState } from 'react'
import Profile from './Profile'

function App() {
  const users = ['Alice', 'Bob', 'Clark']
  const [user, setUser] = useState(users[0])
  const [status, setstatus] = useState(true)

  console.log('App Rendered')

  return (
    <>
      <h2>User Profile</h2>
      <button onClick={() => setstatus(!status)}>
        Toggle Status
      </button>
      <button onClick={
        () => setUser(
          users[(users.indexOf(user) + 1) % users.length]
        )}>
        Switch User
      </button>
      <p>
        <b>{user}</b> | {status ? 'Active' : 'Inactive'}
      </p>

      <Profile name={user} />
    </>
  )
}

export default App;
```

<hr/>

### TempInput.jsx
```js
import React from 'react'

const TempInput = (
  { value, unit, onChange }
) => {
  return (
    <div className='temp-input'>
      <input
        type="number"
        value={value}
        onChange={
          e => onChange(e.target.value)
        }
        placeholder={
          `In ${unit}`
        }
      />
      <span> {unit}</span>
    </div>
  )
}

export default TempInput
```

### UnitSelector.jsx
```js
import React from 'react'

const UnitSelector = ({ unit, onUnitChange }) => {
  return (
    <div className='unit-selector'>
      <label>
        <input
          type="radio"
          value="Celsius"
          checked={unit === "Celsius"}
          onChange={
            e => onUnitChange(e.target.value)}
        />
        Celsius
      </label>
      <label>
        <input
          type="radio"
          value="Fahrenheit"
          checked={unit === "Fahrenheit"}
          onChange={
            e => onUnitChange(e.target.value)}
        />
        Fahrenheit
      </label>
    </div>
  )
}

export default UnitSelector
```

### App.jsx
```js
import './App.css'
import { useState } from 'react'
import TempInput from './TempInput'
import UnitSelector from './UnitSelector'

const App = () => {
  const [temperature, setTemperature] = useState("")
  const [unit, setUnit] = useState("Celsius")

  const convertedTemp = unit === "Celsius"
    ? (temperature * 9/5 + 32).toFixed(1)
    : ((temperature - 32) * 5/9).toFixed(1)

  return (
    <div>
      <h2>Temperature Converter</h2>
      <p>
        Converted: {temperature ? convertedTemp : "--"} 
        {unit === "Celsius" ? "°F" : "°C"}
      </p>
      <TempInput
        value={temperature}
        unit={unit}
        onChange={setTemperature}
      />
      <UnitSelector
        unit={unit}
        onUnitChange={setUnit}
      />
    </div>
  )
}

export default App
```

<hr/>

```js
import './App.css'
import { useState } from 'react'

function Form() {
  const [username, setUsername] = useState('')
  const [isSubscribed, setSubscribed]
   = useState(false)
  const [role, setRole] = useState('user')
  const roles = ['user', 'admin', 'guest']

  return (
    <form>
	    <p>
        Name: {username}
        {isSubscribed && ' (Subscribed)'}
      </p>
      <p>Role: {role}</p>
      <input
        type="text" placeholder="Username"
        value={username}
        onChange={
          (e) => setUsername(e.target.value)
        }/>
      <input
        type="checkbox"
        checked={isSubscribed}
        onChange={
          (e) => setSubscribed(e.target.checked)
          }/>
      <label>Subscribe</label>

      <select value={role} onChange={
        (e) => setRole(e.target.value)}>
        {roles.map((r) => (
          <option key={r} value={r}>
            {r}
          </option>
        ))}
      </select>
    </form>
  )
}

export default Form
```

<hr/>

```js
import './App.css'
import { useState } from 'react'

function Form() {
  const [formData, setFormData] = useState({
    username: '',
    isSubscribed: false,
    role: 'user'
  })
  const roles = ['user', 'admin', 'guest']

  const handleChange = (e) => {
    const { name, value, type, checked }
     = e.target
    setFormData({
      ...formData,
      [name]:  type === 'checkbox' ? checked : value
    })
  }

  return (
    <form>
      <p>
        Name: {formData.username}
        {formData.isSubscribed && ' (Subscribed)'}
      </p>
      <p>Role: {formData.role}</p>
      <input
        type="text"
        name="username"
        placeholder="Username"
        value={formData.username}
        onChange={handleChange}
      />

      <label>
        <input
          type="checkbox"
          name="isSubscribed"
          checked={formData.isSubscribed}
          onChange={handleChange}
        />
        Subscribe
      </label>

      <select 
        name="role" value={formData.role}
        onChange={handleChange}>
        {roles.map((r) => (
          <option key={r} value={r}>
            {r}
          </option>
        ))}
      </select>
    </form>
  )
}

export default Form
```
