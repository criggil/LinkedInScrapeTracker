flowchart TB
    subgraph User_Interface
        UI[Web Interface] --> Settings[Topic/Keyword Settings]
        UI --> Dashboard[Monitoring Dashboard]
        UI --> Notifications[Notification Preferences]
    end

    subgraph Data_Collection
        Scheduler[Scheduling Service] --> ProxyManager[Proxy Rotation Manager]
        ProxyManager --> Scraper[LinkedIn Scraper]
        Scraper --> Parser[HTML Parser]
        Parser --> DataExtractor[Data Extraction Service]
        DataExtractor --> Queue[Processing Queue]
    end

    subgraph Processing_Layer
        Queue --> Processor[Content Processor]
        Processor --> Analyzer[Content Analyzer]
        Analyzer --> Classifier[Topic Classifier]
        Classifier --> Relevance[Relevance Scorer]
        Relevance --> Filter[Duplicate Filter]
    end

    subgraph Storage_Layer
        Filter --> DB[(Database)]
        DB --> Cache[Cache Service]
    end

    subgraph Notification_System
        Trigger[Notification Trigger] --> Generator[Content Generator]
        Generator --> Sender[Notification Sender]
        Sender --> Email[Email Service]
        Sender --> Push[Push Notification Service]
        Sender --> Webhook[Webhook Service]
    end

    User_Interface --Topics Configuration--> Data_Collection
    Storage_Layer --New Content--> Notification_System
    Notification_System --Alerts--> User_Interface
    Processing_Layer --Query Data--> Storage_Layer
    User_Interface --Data Access--> Storage_Layer