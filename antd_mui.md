# MUI vs Ant Design: DatePicker 비교

React UI 라이브러리인 **Material UI(MUI)**와 **Ant Design**의 `DatePicker` 컴포넌트를 기능, 옵션, API 측면에서 비교한 문서입니다.

---

## 비교 표

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
| **모바일 반응형**           | 모바일 대응 좋음 (특히 `MobileDatePicker` 존재)            | 반응형 기본 제공되지만 UI가 데스크톱에 더 최적화됨        |
| **range 지원 여부**         | 별도 `DateRangePicker` 존재 (`@mui/x-date-pickers-pro`)    | `RangePicker` 내장                                          |
| **달력 UI 커스터마이징**    | `slots`, `slotProps`, `PopperProps`, `componentsProps` 등   | `dateRender`, `monthCellRender`, `renderExtraFooter` 등    |
| **오픈 컨트롤**             | `open`, `onOpen`, `onClose`                                | `open`, `onOpenChange`                                     |
| **포커스 제어**             | 기본 input과 동일하게 작동                                 | `autoFocus`, `allowClear` 등 지원                          |
| **입력 마스킹 지원**        | `mask` (ex. `__ / __ / ____`)                              | 없음 (직접 입력 제한은 없음)                              |

---

## MUI DatePicker 사용 예시

```tsx
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
