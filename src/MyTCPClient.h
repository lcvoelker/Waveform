#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Sockets.h"
#include "Networking.h"
#include "MyTCPClient.generated.h"  // ✅ Ensure this is included

UCLASS()
class TEST_API AMyTCPClient : public AActor  // ✅ Updated macro to match project name
{
    GENERATED_BODY()

public:
    AMyTCPClient();

protected:
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;

private:
    FSocket* ClientSocket;
    bool ConnectToServer();
    void ReceiveData();
};
