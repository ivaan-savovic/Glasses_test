import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "/components/ui/card"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "/components/ui/select"
import { Button } from "/components/ui/button"
import { Clock, Home, Settings } from "lucide-react"

type Sensor = {
  id: string
  name: string
  value: number
  unit: string
  icon: JSX.Element
  selected: boolean
}

export default function SensorApp() {
  const [sensors, setSensors] = useState<Sensor[]>([
    {
      id: 'temp',
      name: 'Temperature',
      value: 22.5,
      unit: '°C',
      icon: <Home className="w-5 h-5" />,
      selected: true
    },
    {
      id: 'humidity',
      name: 'Humidity',
      value: 45,
      unit: '%',
      icon: <Settings className="w-5 h-5" />,
      selected: true
    },
    {
      id: 'light',
      name: 'Light Level',
      value: 750,
      unit: 'lux',
      icon: <Clock className="w-5 h-5" />,
      selected: true
    },
    {
      id: 'pressure',
      name: 'Pressure',
      value: 1013,
      unit: 'hPa',
      icon: <Settings className="w-5 h-5" />,
      selected: false
    },
    {
      id: 'uv',
      name: 'UV Index',
      value: 3,
      unit: '',
      icon: <Home className="w-5 h-5" />,
      selected: false
    }
  ])

  // Simulate real-time data updates
  useEffect(() => {
    const interval = setInterval(() => {
      setSensors(prevSensors => prevSensors.map(sensor => ({
        ...sensor,
        value: sensor.selected ? getRandomValue(sensor.id, sensor.value) : sensor.value
      })))
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  const getRandomValue = (id: string, currentValue: number): number => {
    // Small random fluctuation around current value
    const fluctuation = Math.random() * 2 - 1 // Random between -1 and 1
    
    // Different sensors have different ranges and behaviors
    switch(id) {
      case 'temp':
        return Math.max(15, Math.min(35, currentValue + fluctuation * 0.2))
      case 'humidity':
        return Math.max(30, Math.min(80, currentValue + fluctuation * 0.5))
      case 'light':
        return Math.max(0, Math.min(2000, currentValue + fluctuation * 10))
      case 'pressure':
        return Math.max(980, Math.min(1040, currentValue + fluctuation * 0.5))
      case 'uv':
        return Math.max(0, Math.min(11, currentValue + fluctuation * 0.1))
      default:
        return currentValue
    }
  }

  const toggleSensor = (sensorId: string) => {
    setSensors(prevSensors => 
      prevSensors.map(sensor => 
        sensor.id === sensorId 
          ? { ...sensor, selected: !sensor.selected } 
          : sensor
      )
    )
  }

  const visibleSensors = sensors.filter(sensor => sensor.selected)

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Smart Glasses Sensor Dashboard</h1>
          <p className="text-gray-600">Real-time sensor monitoring</p>
        </header>

        <div className="mb-6 flex items-center gap-4">
          <Select onValueChange={toggleSensor}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select sensors" />
            </SelectTrigger>
            <SelectContent>
              {sensors.map(sensor => (
                <SelectItem 
                  key={sensor.id} 
                  value={sensor.id}
                  className={sensor.selected ? 'bg-gray-100' : ''}
                >
                  {sensor.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button variant="outline" className="ml-auto">
            <Settings className="mr-2 h-4 w-4" />
            Settings
          </Button>
        </div>

        {visibleSensors.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500">No sensors selected. Please select sensors to display data.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {visibleSensors.map(sensor => (
              <Card key={sensor.id} className="hover:shadow-lg transition-shadow">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-gray-500">
                    {sensor.name}
                  </CardTitle>
                  <div className="text-gray-400">
                    {sensor.icon}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {sensor.value.toFixed(sensor.unit === '%' ? 0 : 1)}{sensor.unit}
                  </div>
                </CardContent>
                <CardFooter>
                  <div className="text-xs text-gray-500">
                    Updated just now
                  </div>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Smart Glasses Sensor App v1.0</p>
        </div>
      </div>
    </div>
  )
}