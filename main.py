import { useState, useEffect } from 'react'
import { Button } from "/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "/components/ui/card"
import { Input } from "/components/ui/input"
import { Label } from "/components/ui/label"
import { Clock, Thermometer, Newspaper, ListChecks, Users, MessageSquare, Camera, Video, Home, Settings, Mic } from "lucide-react"

type DisplayMode = 'home' | 'time' | 'weather' | 'news' | 'reminders' | 'contacts' | 'sms' | 'camera' | 'video' | 'settings'

export default function SmartGlassesAssistant() {
  const [displayMode, setDisplayMode] = useState<DisplayMode>('home')
  const [voiceCommand, setVoiceCommand] = useState('')
  const [response, setResponse] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [volume, setVolume] = useState(70)
  const [brightness, setBrightness] = useState(80)
  const [smsRecipient, setSmsRecipient] = useState('')
  const [smsMessage, setSmsMessage] = useState('')
  const [photoTaken, setPhotoTaken] = useState(false)
  const [inVideoCall, setInVideoCall] = useState(false)
  const [reminders, setReminders] = useState<string[]>([])
  const [newReminder, setNewReminder] = useState('')
  const [contacts, setContacts] = useState([
    { name: 'John Doe', number: '555-1234' },
    { name: 'Jane Smith', number: '555-5678' }
  ])

  // Simulate small screen size for glasses
  useEffect(() => {
    document.documentElement.style.fontSize = '14px'
    return () => {
      document.documentElement.style.fontSize = ''
    }
  }, [])

  const processCommand = (command: string) => {
    const normalizedCommand = command.toLowerCase().trim()
    setVoiceCommand(command)
    
    if (normalizedCommand.includes('time')) {
      setDisplayMode('time')
      setResponse('Showing current time')
    } 
    else if (normalizedCommand.includes('weather')) {
      setDisplayMode('weather')
      setResponse('Showing weather information')
    }
    else if (normalizedCommand.includes('news')) {
      setDisplayMode('news')
      setResponse('Showing news headlines')
    }
    else if (normalizedCommand.includes('reminder')) {
      setDisplayMode('reminders')
      setResponse('Showing reminders')
    }
    else if (normalizedCommand.includes('contact')) {
      setDisplayMode('contacts')
      setResponse('Showing contacts')
    }
    else if (normalizedCommand.includes('message')) {
      setDisplayMode('sms')
      setResponse('Ready to send message')
    }
    else if (normalizedCommand.includes('photo')) {
      setDisplayMode('camera')
      setResponse('Camera ready')
    }
    else if (normalizedCommand.includes('video call')) {
      setDisplayMode('video')
      setInVideoCall(true)
      setResponse('Starting video call')
    }
    else if (normalizedCommand.includes('settings')) {
      setDisplayMode('settings')
      setResponse('Settings panel')
    }
    else if (normalizedCommand.includes('home')) {
      setDisplayMode('home')
      setResponse('Home screen')
    }
    else {
      setResponse(`Command not recognized`)
    }
  }

  const handleSendSms = () => {
    setResponse(`Message sent to ${smsRecipient}`)
    setSmsRecipient('')
    setSmsMessage('')
    setTimeout(() => setDisplayMode('home'), 1500)
  }

  const takePhoto = () => {
    setPhotoTaken(true)
    setResponse('Photo captured')
    setTimeout(() => {
      setPhotoTaken(false)
      setDisplayMode('home')
    }, 1500)
  }

  const endVideoCall = () => {
    setInVideoCall(false)
    setDisplayMode('home')
    setResponse('Call ended')
  }

  const addReminder = () => {
    if (newReminder.trim()) {
      setReminders([...reminders, newReminder])
      setNewReminder('')
      setResponse('Reminder added')
    }
  }

  const removeReminder = (index: number) => {
    const updatedReminders = [...reminders]
    updatedReminders.splice(index, 1)
    setReminders(updatedReminders)
    setResponse('Reminder removed')
  }

  const simulateVoiceInput = () => {
    setIsListening(true)
    setTimeout(() => {
      const sampleCommands = [
        'Show time',
        'Weather',
        'Contacts',
        'Send message',
        'Take photo',
        'Video call',
        'Settings'
      ]
      const randomCommand = sampleCommands[Math.floor(Math.random() * sampleCommands.length)]
      processCommand(randomCommand)
      setIsListening(false)
    }, 1000)
  }

  const renderDisplay = () => {
    switch (displayMode) {
      case 'home':
        return (
          <div className="grid grid-cols-3 gap-2">
            <Button variant="ghost" className="h-20 flex-col" onClick={() => setDisplayMode('time')}>
              <Clock className="mb-1 h-5 w-5" />
              <span className="text-xs">Time</span>
            </Button>
            <Button variant="ghost" className="h-20 flex-col" onClick={() => setDisplayMode('weather')}>
              <Thermometer className="mb-1 h-5 w-5" />
              <span className="text-xs">Weather</span>
            </Button>
            <Button variant="ghost" className="h-20 flex-col" onClick={() => setDisplayMode('news')}>
              <Newspaper className="mb-1 h-5 w-5" />
              <span className="text-xs">News</span>
            </Button>
            <Button variant="ghost" className="h-20 flex-col" onClick={() => setDisplayMode('reminders')}>
              <ListChecks className="mb-1 h-5 w-5" />
              <span className="text-xs">Reminders</span>
            </Button>
            <Button variant="ghost" className="h-20 flex-col" onClick={() => setDisplayMode('contacts')}>
              <Users className="mb-1 h-5 w-5" />
              <span className="text-xs">Contacts</span>
            </Button>
            <Button variant="ghost" className="h-20 flex-col" onClick={() => setDisplayMode('sms')}>
              <MessageSquare className="mb-1 h-5 w-5" />
              <span className="text-xs">Messages</span>
            </Button>
          </div>
        )
      case 'time':
        return (
          <div className="text-center py-4">
            <p className="text-3xl font-mono font-bold">{new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
            <p className="text-sm mt-1">{new Date().toLocaleDateString([], {weekday: 'short', month: 'short', day: 'numeric'})}</p>
          </div>
        )
      case 'weather':
        return (
          <div className="text-center py-2">
            <div className="bg-blue-100 rounded-full w-12 h-12 mx-auto mb-2 flex items-center justify-center">
              <Thermometer className="h-6 w-6 text-blue-600" />
            </div>
            <p className="text-2xl font-bold">22°C</p>
            <p className="text-sm">Sunny</p>
            <p className="text-xs text-gray-500 mt-1">Zagreb, HR</p>
          </div>
        )
      case 'news':
        return (
          <div className="space-y-3 py-1">
            <div className="bg-gray-100 p-2 rounded">
              <p className="text-xs font-medium">Tech: New AI breakthrough</p>
            </div>
            <div className="bg-gray-100 p-2 rounded">
              <p className="text-xs font-medium">Sports: World Cup results</p>
            </div>
            <div className="bg-gray-100 p-2 rounded">
              <p className="text-xs font-medium">Finance: Market update</p>
            </div>
          </div>
        )
      case 'reminders':
        return (
          <div className="space-y-2 py-1">
            <div className="flex gap-1">
              <Input 
                value={newReminder}
                onChange={(e) => setNewReminder(e.target.value)}
                placeholder="New reminder"
                className="h-8 text-xs"
              />
              <Button onClick={addReminder} className="h-8 px-2">
                Add
              </Button>
            </div>
            {reminders.length > 0 ? (
              <ul className="space-y-1">
                {reminders.map((reminder, index) => (
                  <li key={index} className="flex justify-between items-center bg-gray-100 p-2 rounded text-xs">
                    <span className="truncate">{reminder}</span>
                    <Button 
                      variant="ghost" 
                      size="sm"
                      className="h-6 w-6 p-0"
                      onClick={() => removeReminder(index)}
                    >
                      ×
                    </Button>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-center py-2">No reminders</p>
            )}
          </div>
        )
      case 'contacts':
        return (
          <div className="space-y-1 py-1">
            {contacts.map((contact, index) => (
              <div key={index} className="flex justify-between items-center bg-gray-100 p-2 rounded">
                <div>
                  <p className="text-xs font-medium">{contact.name}</p>
                  <p className="text-xs text-gray-500">{contact.number}</p>
                </div>
                <Button variant="ghost" size="sm" className="h-6 text-xs">
                  Call
                </Button>
              </div>
            ))}
          </div>
        )
      case 'sms':
        return (
          <div className="space-y-2 py-1">
            <div className="space-y-1">
              <Label className="text-xs">To:</Label>
              <Input 
                value={smsRecipient}
                onChange={(e) => setSmsRecipient(e.target.value)}
                placeholder="Number"
                className="h-8 text-xs"
              />
            </div>
            <div className="space-y-1">
              <Label className="text-xs">Message:</Label>
              <Input 
                value={smsMessage}
                onChange={(e) => setSmsMessage(e.target.value)}
                placeholder="Type message"
                className="h-8 text-xs"
              />
            </div>
            <Button onClick={handleSendSms} className="h-8 w-full text-xs">
              Send
            </Button>
          </div>
        )
      case 'camera':
        return (
          <div className="text-center py-2">
            <div className="bg-black rounded-md w-full h-32 mb-2 flex items-center justify-center">
              {photoTaken ? (
                <p className="text-white text-xs">Photo saved</p>
              ) : (
                <div className="border-2 border-white rounded-full w-8 h-8"></div>
              )}
            </div>
            <Button 
              onClick={takePhoto} 
              className="h-8 w-20 mx-auto text-xs"
              disabled={photoTaken}
            >
              {photoTaken ? 'Done' : 'Capture'}
            </Button>
          </div>
        )
      case 'video':
        return (
          <div className="text-center py-2">
            <div className="bg-black rounded-md w-full h-32 mb-2 flex items-center justify-center">
              {inVideoCall ? (
                <div className="relative w-full h-full">
                  <div className="absolute bottom-1 right-1 bg-gray-800 rounded w-16 h-10 flex items-center justify-center">
                    <p className="text-white text-xs">You</p>
                  </div>
                </div>
              ) : (
                <p className="text-white text-xs">Call ended</p>
              )}
            </div>
            {inVideoCall ? (
              <Button 
                onClick={endVideoCall} 
                variant="destructive"
                className="h-8 w-20 mx-auto text-xs"
              >
                End
              </Button>
            ) : (
              <Button 
                onClick={() => setInVideoCall(true)}
                className="h-8 w-20 mx-auto text-xs"
              >
                Call
              </Button>
            )}
          </div>
        )
      case 'settings':
        return (
          <div className="space-y-3 py-1">
            <div>
              <Label className="text-xs flex justify-between">
                <span>Volume</span>
                <span>{volume}%</span>
              </Label>
              <input
                type="range"
                min="0"
                max="100"
                value={volume}
                onChange={(e) => setVolume(parseInt(e.target.value))}
                className="w-full h-1"
              />
            </div>
            <div>
              <Label className="text-xs flex justify-between">
                <span>Brightness</span>
                <span>{brightness}%</span>
              </Label>
              <input
                type="range"
                min="0"
                max="100"
                value={brightness}
                onChange={(e) => setBrightness(parseInt(e.target.value))}
                className="w-full h-1"
              />
            </div>
          </div>
        )
      default:
        return <p>Select a mode</p>
    }
  }

  return (
    <div className="fixed inset-0 bg-black text-white flex items-center justify-center p-2">
      <div className="w-full max-w-sm bg-gray-900 rounded-lg overflow-hidden border border-gray-700">
        {/* Status bar */}
        <div className="flex justify-between items-center px-3 py-1 bg-gray-800 text-xs">
          <span>9:41</span>
          <div className="flex items-center space-x-2">
            <span>100%</span>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
        </div>

        {/* Main content */}
        <div className="p-3">
          {/* Command feedback */}
          {(voiceCommand || response) && (
            <div className="bg-gray-800 p-2 rounded mb-2 text-xs">
              {voiceCommand && <p className="font-medium">"{voiceCommand}"</p>}
              {response && <p className="text-blue-400">{response}</p>}
            </div>
          )}

          {/* Display area */}
          <div className="min-h-40 mb-3">
            {renderDisplay()}
          </div>

          {/* Navigation controls */}
          <div className="flex justify-between">
            <Button 
              variant="ghost" 
              size="sm"
              className="text-xs h-8"
              onClick={() => setDisplayMode('home')}
            >
              <Home className="mr-1 h-3 w-3" /> Home
            </Button>
            <Button 
              variant={isListening ? 'default' : 'ghost'} 
              size="sm"
              className="text-xs h-8"
              onClick={simulateVoiceInput}
            >
              <Mic className="mr-1 h-3 w-3" /> {isListening ? 'Listening...' : 'Voice'}
            </Button>
            <Button 
              variant="ghost" 
              size="sm"
              className="text-xs h-8"
              onClick={() => setDisplayMode('settings')}
            >
              <Settings className="mr-1 h-3 w-3" /> Settings
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}