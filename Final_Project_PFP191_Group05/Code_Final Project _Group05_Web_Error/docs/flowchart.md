flowchart TD
    A[Người dùng truy cập hệ thống] --> B{Đã đăng nhập?}
    B -->|Chưa| C[Trang đăng nhập]
    B -->|Rồi| D{Vai trò người dùng}
    
    C --> E[Nhập username/password]
    E --> F{Thông tin hợp lệ?}
    F -->|Không| G[Hiển thị lỗi]
    G --> C
    F -->|Có| H[Xác thực thành công]
    H --> D
    
    D -->|Admin| I[Admin Dashboard]
    D -->|Organizer| J[Organizer Dashboard]
    D -->|Student/Visitor| K[Student Dashboard]
    
    %% Admin Flow
    I --> L{Chọn chức năng}
    L --> M[Quản lý tất cả sự kiện]
    L --> N[Quản lý người dùng]
    L --> O[Xem báo cáo tổng quan]
    L --> P[Xuất báo cáo]
    
    M --> M1[Tạo sự kiện mới]
    M --> M2[Sửa/Xóa sự kiện]
    M --> M3[Xem danh sách đăng ký]
    
    %% Organizer Flow
    J --> Q{Chọn chức năng}
    Q --> R[Quản lý sự kiện của tôi]
    Q --> S[Xem thống kê sự kiện]
    
    R --> R1[Tạo sự kiện mới]
    R --> R2[Sửa sự kiện của tôi]
    R --> R3[Xem người đăng ký]
    R --> R4[Quản lý sức chứa]
    
    %% Student/Visitor Flow
    K --> T{Chọn chức năng}
    T --> U[Xem danh sách sự kiện]
    T --> V[Tìm kiếm sự kiện]
    T --> W[Xem sự kiện đã đăng ký]
    
    U --> U1[Lọc theo danh mục]
    U --> U2[Xem chi tiết sự kiện]
    U2 --> U3{Muốn đăng ký?}
    U3 -->|Có| U4{Còn chỗ trống?}
    U4 -->|Có| U5[Đăng ký thành công]
    U4 -->|Hết| U6[Thông báo hết chỗ]
    U3 -->|Không| U
    
    V --> V1[Nhập từ khóa tìm kiếm]
    V1 --> V2[Hiển thị kết quả]
    V2 --> U2
    
    W --> W1[Danh sách đã đăng ký]
    W1 --> W2{Muốn hủy đăng ký?}
    W2 -->|Có| W3[Hủy đăng ký thành công]
    W2 -->|Không| W
    
    %% Event Creation Process
    M1 --> EC1[Nhập thông tin sự kiện]
    R1 --> EC1
    EC1 --> EC2{Dữ liệu hợp lệ?}
    EC2 -->|Không| EC3[Hiển thị lỗi validation]
    EC3 --> EC1
    EC2 -->|Có| EC4[Lưu sự kiện vào database]
    EC4 --> EC5[Thông báo tạo thành công]
    
    %% Registration Process
    U5 --> REG1[Kiểm tra đăng ký trùng lặp]
    REG1 --> REG2{Đã đăng ký trước?}
    REG2 -->|Có| REG3[Thông báo đã đăng ký]
    REG2 -->|Chưa| REG4[Tạo bản ghi đăng ký]
    REG4 --> REG5[Cập nhật số lượng tham gia]
    REG5 --> REG6[Gửi email xác nhận]
    REG6 --> REG7[Hoàn thành đăng ký]
    
    %% Data Management
    EC4 --> DATA1[(Database JSON)]
    REG4 --> DATA1
    W3 --> DATA1
    
    DATA1 --> DATA2[users.json]
    DATA1 --> DATA3[events.json]
    DATA1 --> DATA4[registrations.json]
    
    %% Report Generation
    P --> RP1[Chọn loại báo cáo]
    RP1 --> RP2{Báo cáo sự kiện?}
    RP2 -->|Có| RP3[Xuất events.csv]
    RP2 -->|Không| RP4[Xuất registrations.csv]
    
    %% Logout Process
    I --> LO[Đăng xuất]
    J --> LO
    K --> LO
    LO --> LO1[Xóa session]
    LO1 --> LO2[Chuyển về trang chủ]
    
    %% Styling
    classDef adminClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef organizerClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef studentClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef processClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef dataClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    
    class I,L,M,N,O,P,M1,M2,M3 adminClass
    class J,Q,R,S,R1,R2,R3,R4 organizerClass
    class K,T,U,V,W,U1,U2,U3,U4,U5,U6,V1,V2,W1,W2,W3 studentClass
    class EC1,EC2,EC3,EC4,EC5,REG1,REG2,REG3,REG4,REG5,REG6,REG7,RP1,RP2,RP3,RP4 processClass
    class DATA1,DATA2,DATA3,DATA4 dataClass