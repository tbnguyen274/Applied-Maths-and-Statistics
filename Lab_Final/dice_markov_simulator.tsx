import React, { useState, useEffect } from 'react';
import { Dice1, Dice2, Dice3, Dice4, Dice5, Dice6, Play, Pause, RotateCcw, BarChart3 } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar, ResponsiveContainer } from 'recharts';

const DiceMarkovSimulator = () => {
  const [currentState, setCurrentState] = useState(0);
  const [sum, setSum] = useState(0);
  const [rollCount, setRollCount] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [speed, setSpeed] = useState(500);
  const [history, setHistory] = useState([]);
  const [stateFrequency, setStateFrequency] = useState(Array(7).fill(0));
  const [lastRoll, setLastRoll] = useState(null);
  
  // Ma trận chuyển trạng thái
  const transitionMatrix = [
    [0, 1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
    [1/6, 0, 1/6, 1/6, 1/6, 1/6, 1/6],
    [1/6, 1/6, 0, 1/6, 1/6, 1/6, 1/6],
    [1/6, 1/6, 1/6, 0, 1/6, 1/6, 1/6],
    [1/6, 1/6, 1/6, 1/6, 0, 1/6, 1/6],
    [1/6, 1/6, 1/6, 1/6, 1/6, 0, 1/6],
    [1/6, 1/6, 1/6, 1/6, 1/6, 1/6, 0]
  ];

  const getDiceIcon = (value) => {
    const icons = [null, Dice1, Dice2, Dice3, Dice4, Dice5, Dice6];
    const Icon = icons[value];
    return Icon ? <Icon className="w-8 h-8 text-blue-600" /> : null;
  };

  const rollDice = () => {
    const roll = Math.floor(Math.random() * 6) + 1;
    const newSum = sum + roll;
    const newState = newSum % 7;
    
    setLastRoll(roll);
    setSum(newSum);
    setCurrentState(newState);
    setRollCount(prev => prev + 1);
    
    // Cập nhật lịch sử
    setHistory(prev => [...prev, { step: rollCount + 1, state: newState, sum: newSum, roll }]);
    
    // Cập nhật tần suất
    setStateFrequency(prev => {
      const newFreq = [...prev];
      newFreq[newState]++;
      return newFreq;
    });
  };

  const reset = () => {
    setCurrentState(0);
    setSum(0);
    setRollCount(0);
    setHistory([]);
    setStateFrequency(Array(7).fill(0));
    setLastRoll(null);
    setIsRunning(false);
  };

  const toggleSimulation = () => {
    setIsRunning(!isRunning);
  };

  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(rollDice, speed);
    }
    return () => clearInterval(interval);
  }, [isRunning, speed, sum, rollCount]);

  // Tính phân phối hiện tại
  const currentDistribution = stateFrequency.map(freq => 
    rollCount > 0 ? (freq / rollCount * 100).toFixed(1) : 0
  );

  // Phân phối lý thuyết (1/7 ≈ 14.29%)
  const theoreticalDistribution = Array(7).fill(14.29);

  // Dữ liệu cho biểu đồ
  const distributionData = Array(7).fill().map((_, i) => ({
    state: i,
    observed: parseFloat(currentDistribution[i]),
    theoretical: theoreticalDistribution[i],
    frequency: stateFrequency[i]
  }));

  const chartData = history.slice(-50).map((item, index) => ({
    step: item.step,
    state: item.state
  }));

  return (
    <div className="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          Mô phỏng Xích Markov - Bài toán Xúc xắc
        </h1>
        <p className="text-gray-600 mb-4">
          Mô phỏng quá trình tung xúc xắc và theo dõi phần dư của tổng khi chia cho 7
        </p>

        {/* Điều khiển */}
        <div className="flex flex-wrap gap-4 items-center mb-6">
          <button
            onClick={rollCount === 0 ? rollDice : toggleSimulation}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium ${
              isRunning 
                ? 'bg-red-500 hover:bg-red-600 text-white' 
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            }`}
          >
            {isRunning ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            {rollCount === 0 ? 'Bắt đầu' : (isRunning ? 'Tạm dừng' : 'Tiếp tục')}
          </button>

          <button
            onClick={rollDice}
            disabled={isRunning}
            className="flex items-center gap-2 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium disabled:opacity-50"
          >
            Tung 1 lần
          </button>

          <button
            onClick={reset}
            className="flex items-center gap-2 px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg font-medium"
          >
            <RotateCcw className="w-4 h-4" />
            Reset
          </button>

          <div className="flex items-center gap-2">
            <label className="text-sm font-medium">Tốc độ:</label>
            <select
              value={speed}
              onChange={(e) => setSpeed(parseInt(e.target.value))}
              className="px-3 py-1 border rounded-md"
            >
              <option value={100}>Rất nhanh</option>
              <option value={300}>Nhanh</option>
              <option value={500}>Vừa</option>
              <option value={1000}>Chậm</option>
            </select>
          </div>
        </div>

        {/* Trạng thái hiện tại */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-blue-600">{rollCount}</div>
            <div className="text-sm text-gray-600">Số lần tung</div>
          </div>
          
          <div className="bg-green-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-green-600">{sum}</div>
            <div className="text-sm text-gray-600">Tổng S₍ₙ₎</div>
          </div>
          
          <div className="bg-purple-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-purple-600">{currentState}</div>
            <div className="text-sm text-gray-600">Trạng thái Xₙ</div>
          </div>
          
          <div className="bg-orange-50 p-4 rounded-lg text-center flex flex-col items-center">
            <div className="mb-2">
              {lastRoll && getDiceIcon(lastRoll)}
            </div>
            <div className="text-sm text-gray-600">Lần tung cuối</div>
          </div>
        </div>
      </div>

      {/* Biểu đồ */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Biểu đồ phân phối */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            Phân phối trạng thái
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={distributionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="state" />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [
                  name === 'observed' ? `${value}%` : `${value}%`,
                  name === 'observed' ? 'Quan sát' : 'Lý thuyết'
                ]}
              />
              <Legend />
              <Bar dataKey="observed" fill="#3B82F6" name="Quan sát" />
              <Bar dataKey="theoretical" fill="#EF4444" name="Lý thuyết (1/7)" opacity={0.7} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Biểu đồ lịch sử trạng thái */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold mb-4">Lịch sử trạng thái (50 bước gần nhất)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="step" />
              <YAxis domain={[0, 6]} />
              <Tooltip />
              <Line 
                type="stepAfter" 
                dataKey="state" 
                stroke="#3B82F6" 
                strokeWidth={2}
                dot={{ fill: '#3B82F6', strokeWidth: 2, r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Ma trận chuyển trạng thái */}
      <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
        <h3 className="text-xl font-semibold mb-4">Ma trận chuyển trạng thái P</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr>
                <th className="p-2 border bg-gray-50">Từ\Đến</th>
                {Array(7).fill().map((_, i) => (
                  <th key={i} className="p-2 border bg-gray-50">{i}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {transitionMatrix.map((row, i) => (
                <tr key={i}>
                  <td className="p-2 border bg-gray-50 font-medium">{i}</td>
                  {row.map((prob, j) => (
                    <td 
                      key={j} 
                      className={`p-2 border text-center ${
                        prob > 0 ? 'bg-blue-50' : 'bg-gray-100'
                      }`}
                    >
                      {prob > 0 ? '1/6' : '0'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-sm text-gray-600 mt-2">
          <strong>Lưu ý:</strong> Mỗi cột có tổng = 1. Xác suất chuyển từ trạng thái j đến các trạng thái khác.
        </p>
      </div>

      {/* Thống kê */}
      {rollCount > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
          <h3 className="text-xl font-semibold mb-4">Thống kê chi tiết</h3>
          <div className="grid grid-cols-7 gap-4">
            {Array(7).fill().map((_, i) => (
              <div key={i} className="text-center">
                <div className="text-2xl font-bold text-blue-600">{stateFrequency[i]}</div>
                <div className="text-sm text-gray-600">Trạng thái {i}</div>
                <div className="text-xs text-gray-500">{currentDistribution[i]}%</div>
              </div>
            ))}
          </div>
          <div className="mt-4 text-sm text-gray-600">
            <p><strong>Phân phối lý thuyết:</strong> Mỗi trạng thái có xác suất 1/7 ≈ 14.29%</p>
            <p><strong>Độ lệch trung bình:</strong> {
              rollCount > 0 ? 
                (currentDistribution.reduce((sum, obs) => sum + Math.abs(obs - 14.29), 0) / 7).toFixed(2) 
                : 0
            }%</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default DiceMarkovSimulator;