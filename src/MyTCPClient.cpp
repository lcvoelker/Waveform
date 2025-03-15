#include "MyTCPClient.h"
#include "Sockets.h"
#include "SocketSubsystem.h"
#include "Networking.h"

AMyTCPClient::AMyTCPClient()
{
    PrimaryActorTick.bCanEverTick = true;
}

void AMyTCPClient::BeginPlay()
{
    Super::BeginPlay();

    UE_LOG(LogTemp, Warning, TEXT("Attempting to connect to Python server..."));

    if (ConnectToServer())
    {
        UE_LOG(LogTemp, Warning, TEXT("Connected to Python server successfully."));
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to connect to Python server."));
    }
}

bool AMyTCPClient::ConnectToServer()
{
    // Create the socket
    ClientSocket = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->CreateSocket(NAME_Stream, TEXT("TCP_CLIENT"), false);

    if (!ClientSocket)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to create socket."));
        return false;
    }

    // Set the server address (should match the Python script)
    FIPv4Address Addr;
    FIPv4Address::Parse(TEXT("127.0.0.1"), Addr);
    FIPv4Endpoint Endpoint(Addr, 5000);

    // Connect to Python server
    bool Connected = ClientSocket->Connect(Endpoint.ToInternetAddr().Get());

    return Connected;
}

void AMyTCPClient::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    ReceiveData();
}

void AMyTCPClient::ReceiveData()
{
    if (!ClientSocket) return;

    uint32 DataSize;
    if (ClientSocket->HasPendingData(DataSize))
    {
        TArray<uint8> ReceivedData;
        ReceivedData.SetNumUninitialized(DataSize);
        int32 Read = 0;
        ClientSocket->Recv(ReceivedData.GetData(), ReceivedData.Num(), Read);

        FString ReceivedString = FString(ANSI_TO_TCHAR(reinterpret_cast<const char>(ReceivedData.GetData())));
        UE_LOG(LogTemp, Warning, TEXT("Received Data: %s"),ReceivedString);
    }
}
