# MUI vs Ant Design: DatePicker 기능 비교

React UI 라이브러리인 **Material UI (MUI)**와 **Ant Design (Antd)**의 `DatePicker` 컴포넌트 기능, 옵션, API 차이점을 정리한 문서입니다.

---

## 기본 정보 비교

| 항목                          | **MUI (Material UI)**                                       | **Ant Design**                                              |
|-----------------------------|--------------------------------------------------------------|-------------------------------------------------------------|
| **기본 컴포넌트 이름**       | `DatePicker` (`@mui/x-date-pickers`)                        | `DatePicker` (`antd`)                                      |
| **설치 패키지**              | `@mui/x-date-pickers`, `@mui/material`, `@date-io` 등 필요 | `antd`                                                      |
| **날짜 포맷**               | `format` (Day.js, Luxon, date-fns 등과 연동)               | `format` (moment.js 기반, dayjs로도 교체 가능)            |
| **기본 값 설정**            | `value`, `defaultValue`                                     | `value`, `defaultValue`                                     |
| **변경 이벤트**             | `onChange(date: Dayjs \| null)`                             | `onChange(date: moment \| string)`                          |
| **disable 설정**            | `disabled`, `shouldDisableDate`                            | `disabledDate`, `disabledTime`, `disabled`                  |
| **min/max 날짜 제한**       | `minDate`, `maxDate`                                       | `disabledDate: (date) => boolean` 방식으로 커스터마이징   |
| **입력 포맷 설정**          | `inputFormat`, `mask`, `format`                            | `format` (단일 설정)                                        |
| **시간 선택 지원**          | 별도 `DateTimePicker` 컴포넌트 사용                        | `showTime` 옵션 사용 (`DatePicker`에서 시간 선택 포함)     |
| **다국어/로케일 지원**      | `LocalizationProvider` 사용                                | `ConfigProvider` 사용                                       |
| **렌더 커스터마이징**       | `renderInput`, `slots` 등으로 TextField 커스터마이징      | `renderExtraFooter`, `suffixIcon`, `dropdownClassName` 등 |
| **모바일 반응형**           | 모바일 대응 좋음 (`MobileDatePicker` 존재)                 | 반응형 제공되지만 데스크톱에 최적화됨                      |
| **range 지원 여부**         | `DateRangePicker` (Pro 패키지 필요)                        | `RangePicker` 내장                                          |
| **달력 UI 커스터마이징**    | `slots`, `slotProps`, `PopperProps`, `componentsProps` 등   | `dateRender`, `monthCellRender`, `renderExtraFooter` 등    |
| **오픈 컨트롤**             | `open`, `onOpen`, `onClose`                                | `open`, `onOpenChange`                                     |
| **포커스 제어**             | 기본 input과 동일하게 작동                                 | `autoFocus`, `allowClear` 등 지원                          |
| **입력 마스킹 지원**        | `mask` (ex. `__ / __ / ____`)                              | 없음 (직접 입력 제한은 없음)                              |

---

## MUI DatePicker 예제

```tsx
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs from 'dayjs';
import TextField from '@mui/material/TextField';

<DatePicker
  label="Select date"
  value={value}
  onChange={(newValue) => setValue(newValue)}
  minDate={dayjs().subtract(1, 'year')}
  maxDate={dayjs().add(1, 'year')}
  disableFuture
  format="YYYY/MM/DD"
  renderInput={(params) => <TextField {...params} />}
/>
```

---

## Ant Design DatePicker 예제

```tsx
import { DatePicker } from 'antd';
import moment from 'moment';

<DatePicker
  value={value}
  onChange={(date, dateString) => setValue(date)}
  format="YYYY/MM/DD"
  disabledDate={(current) => current && current > moment().endOf('day')}
  showTime
  allowClear
/>
```

---

## 주요 차이 요약

- **날짜 처리 라이브러리**  
  - MUI: `dayjs`, `date-fns`, `luxon` 등 선택 가능  
  - Ant Design: `moment.js` 기본, `dayjs`로 대체 가능

- **시간 선택**  
  - MUI: `DateTimePicker` 별도 제공  
  - Ant Design: `showTime` 옵션으로 시간 포함 가능

- **범위 선택**  
  - MUI: `DateRangePicker` (Pro 패키지)  
  - Ant Design: `RangePicker` 기본 포함

- **커스터마이징 방식**  
  - MUI: `slots`, `renderInput` 중심  
  - Ant Design: `dateRender`, `renderExtraFooter` 중심

---

> 필요한 경우 스타일 커스터마이징 비교나 코드 샘플을 더 추가할 수 있습니다.
