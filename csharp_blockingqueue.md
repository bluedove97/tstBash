# 예시 코드
## 일반
### 1. 전역 큐 정의
```csharp
using System.Collections.Concurrent;

public static class GlobalQueue
{
    public static BlockingCollection<string> Queue 
        = new BlockingCollection<string>(new ConcurrentQueue<string>());
}
```

### 2. 미들웨어나 백그라운드에서 생산자
```csharp
public class ProducerService
{
    private readonly CancellationTokenSource _cts = new CancellationTokenSource();

    public void Start()
    {
        Task.Run(async () =>
        {
            int count = 0;
            while (!_cts.Token.IsCancellationRequested)
            {
                var item = $"Job-{++count}";
                GlobalQueue.Queue.Add(item);
                Console.WriteLine($"[Producer] Added: {item}");
                await Task.Delay(1000); // 1초마다 데이터 생성
            }
        });
    }

    public void Stop()
    {
        _cts.Cancel();
        GlobalQueue.Queue.CompleteAdding();
    }
}
```

### 3. Startup에서 생산자 실행
```csharp
public class Startup
{
    private static ProducerService _producer;

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        _producer = new ProducerService();
        _producer.Start();

        if (env.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }

        app.UseRouting();
        app.UseEndpoints(endpoints =>
        {
            endpoints.MapControllers();
        });
    }

    public void Stop()
    {
        _producer?.Stop();
    }
}
```

### 4. Controller에서 소비자 역할
```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("[controller]")]
public class JobController : ControllerBase
{
    [HttpGet("dequeue")]
    public IActionResult Dequeue()
    {
        if (GlobalQueue.Queue.TryTake(out var item))
        {
            return Ok(new { item });
        }
        else
        {
            return NotFound("Queue is empty");
        }
    }
}
```

### 작동 흐름
- 서버 시작 시 ProducerService가 계속 큐에 데이터 쌓음.
- 클라이언트가 /job/dequeue 호출 시 큐에서 하나 꺼내서 반환.
- 큐가 비어 있으면 NotFound 반환.

## 미들웨어에서 바로 생산
### 1. 전역 큐 정의
```csharp
using System.Collections.Concurrent;

public static class GlobalQueue
{
    public static BlockingCollection<string> Queue 
        = new BlockingCollection<string>(new ConcurrentQueue<string>());
}
```
### 2. 미들웨어에서 생산자 역할
```csharp
public class ProducerMiddleware
{
    private readonly RequestDelegate _next;

    public ProducerMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // 매 요청마다 생산자 역할
        var item = $"Job-{DateTime.Now:HHmmssfff}";
        GlobalQueue.Queue.Add(item);
        Console.WriteLine($"[ProducerMiddleware] Added: {item}");

        // 다음 미들웨어 실행
        await _next(context);
    }
}
```

### 3. Startup에서 미들웨어 등록
```csharp
public class Startup
{
    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        if (env.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }

        // 미들웨어 등록 (가장 앞단에서 실행)
        app.UseMiddleware<ProducerMiddleware>();

        app.UseRouting();

        app.UseEndpoints(endpoints =>
        {
            endpoints.MapControllers();
        });
    }
}
```

### 4. Controller에서 소비자 역할
```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("[controller]")]
public class JobController : ControllerBase
{
    [HttpGet("dequeue")]
    public IActionResult Dequeue()
    {
        if (GlobalQueue.Queue.TryTake(out var item))
        {
            return Ok(new { item });
        }
        else
        {
            return NotFound("Queue is empty");
        }
    }
}
```

### 동작 흐름
- 모든 요청이 ProducerMiddleware를 거치면서 전역 큐에 새로운 아이템 추가
- /job/dequeue를 호출하면 큐에서 하나 꺼내서 반환
- 큐가 비어 있으면 NotFound

```
using System.Collections.Concurrent;

public static class UserQueueManager
{
    private static readonly ConcurrentDictionary<string, BlockingCollection<string>> _queues 
        = new ConcurrentDictionary<string, BlockingCollection<string>>();

    public static BlockingCollection<string> GetQueue(string userId)
    {
        return _queues.GetOrAdd(userId, _ => new BlockingCollection<string>(new ConcurrentQueue<string>()));
    }
}
```

```
public class ProducerMiddleware
{
    private readonly RequestDelegate _next;

    public ProducerMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // 예시: userId를 헤더에서 받는다고 가정
        var userId = context.Request.Headers["X-User-Id"].ToString();
        if (!string.IsNullOrWhiteSpace(userId))
        {
            var queue = UserQueueManager.GetQueue(userId);
            var item = $"Job-{DateTime.Now:HHmmssfff}";
            queue.Add(item);
            Console.WriteLine($"[Producer] User:{userId}, Added:{item}");
        }

        await _next(context);
    }
}
```


```
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("[controller]")]
public class JobController : ControllerBase
{
    [HttpGet("dequeue/{userId}")]
    public IActionResult Dequeue(string userId)
    {
        var queue = UserQueueManager.GetQueue(userId);

        if (queue.TryTake(out var item))
        {
            return Ok(new { userId, item });
        }
        else
        {
            return NotFound($"Queue for user {userId} is empty");
        }
    }
}
```
