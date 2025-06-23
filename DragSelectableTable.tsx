import React, { useState, useRef } from "react";
import { Table } from "antd";
import type { ColumnsType } from "antd/es/table";

interface DataType {
  key: string;
  name: string;
  age: number;
  address: string;
}

const initialData: DataType[] = [
  { key: "1", name: "홍길동", age: 32, address: "서울" },
  { key: "2", name: "김철수", age: 42, address: "부산" },
  { key: "3", name: "이영희", age: 29, address: "인천" },
  { key: "4", name: "박영수", age: 38, address: "대전" },
];

const DragSelectableTable: React.FC = () => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const dragAction = useRef<"select" | "deselect" | null>(null);

  const handleCheckboxChange = (key: string, checked: boolean) => {
    setSelectedRowKeys(prev =>
      checked ? [...prev, key] : prev.filter(k => k !== key)
    );
  };

  const handleMouseDown = (key: string) => {
    const isSelected = selectedRowKeys.includes(key);
    dragAction.current = isSelected ? "deselect" : "select";
    setIsDragging(true);
    handleCheckboxChange(key, dragAction.current === "select");
  };

  const handleMouseEnter = (key: string) => {
    if (!isDragging || !dragAction.current) return;
    handleCheckboxChange(key, dragAction.current === "select");
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    dragAction.current = null;
  };

  const columns: ColumnsType<DataType> = [
    {
      title: "",
      dataIndex: "checkbox",
      width: 50,
      render: (_, record) => (
        <input
          type="checkbox"
          checked={selectedRowKeys.includes(record.key)}
          onChange={(e) =>
            handleCheckboxChange(record.key, e.target.checked)
          }
          onMouseDown={() => handleMouseDown(record.key)}
          onMouseEnter={() => handleMouseEnter(record.key)}
          onMouseUp={handleMouseUp}
        />
      ),
    },
    {
      title: "이름",
      dataIndex: "name",
    },
    {
      title: "나이",
      dataIndex: "age",
    },
    {
      title: "주소",
      dataIndex: "address",
    },
  ];

  return (
    <div
      onMouseUp={handleMouseUp} // 드래그 종료 처리
    >
      <Table
        columns={columns}
        dataSource={initialData}
        pagination={false}
        rowKey="key"
      />
    </div>
  );
};

export default DragSelectableTable;
