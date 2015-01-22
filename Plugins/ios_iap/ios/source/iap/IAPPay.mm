//
//  IAPPay.m
//  sgz
//
//  Created by apple on 14/12/17.
//
//

#import "IAPPay.h"
#include "cocos2d.h"

@implementation IAPPay

static IAPPay * gInstance = nil;

+ (IAPPay *)ShareInstance
{
    if(!gInstance)
    {
        gInstance = [[IAPPay alloc] init];
        [[SKPaymentQueue defaultQueue] addTransactionObserver:gInstance];
    }
    return gInstance;
}

-(BOOL)canMakePayments
{
    return [SKPaymentQueue canMakePayments];
}

-(void)buyWithProduceId:(NSString *)proid
{
    NSArray* transactions = [SKPaymentQueue defaultQueue].transactions;
    if (transactions.count > 0) {
        //检测是否有未完成的交易
        SKPaymentTransaction* transaction = [transactions firstObject];
        if (transaction.transactionState == SKPaymentTransactionStatePurchased) {
            //[self completeTransaction:transaction];
            [[SKPaymentQueue defaultQueue] finishTransaction:transaction];
        }  
    }
    
    NSSet * set = [NSSet setWithArray:@[proid]];
    SKProductsRequest * request = [[SKProductsRequest alloc] initWithProductIdentifiers:set];
    request.delegate = self;
    [request start];
}

-(void)productsRequest:(SKProductsRequest *)request didReceiveResponse:(SKProductsResponse *)response
{
    NSArray *myProduct = response.products;
    if (myProduct.count == 0) {
        NSLog(@"无法获取产品信息，购买失败。");
        cocos2d::CCNotificationCenter::sharedNotificationCenter()->postNotification("IAP_MSG");
        return;
    }
    SKPayment * payment = [SKPayment paymentWithProduct:myProduct[0]];
    [[SKPaymentQueue defaultQueue] addPayment:payment];
}

-(void)paymentQueue:(SKPaymentQueue *)queue updatedTransactions:(NSArray *)transactions
{
    for (SKPaymentTransaction *transaction in transactions)
    {
        switch (transaction.transactionState)
        {
            case SKPaymentTransactionStatePurchased://交易完成
                [self completeTransaction:transaction];
                break;
            case SKPaymentTransactionStateFailed://交易失败
                [self failedTransaction:transaction];
                break;
            case SKPaymentTransactionStateRestored://已经购买过该商品
                [self restoreTransaction:transaction];
                break;
            case SKPaymentTransactionStatePurchasing:      //商品添加进列表
                NSLog(@"商品添加进列表");
                break;
            default:
                break;
        }
    }
}

- (void)completeTransaction:(SKPaymentTransaction *)transaction {
   // NSString *product = transaction.payment.productIdentifier;
    NSLog(@"购买成功,order:%@",transaction.transactionIdentifier);
    cocos2d::CCString *pTemp = cocos2d::CCString::createWithFormat("%s",transaction.transactionIdentifier.UTF8String);
    cocos2d::CCNotificationCenter::sharedNotificationCenter()->postNotification("IAP_MSG",pTemp);
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
    
}
- (void)failedTransaction:(SKPaymentTransaction *)transaction {
    if(transaction.error.code != SKErrorPaymentCancelled) {
        NSLog(@"购买失败");
    } else {
        NSLog(@"用户取消交易");
    }
    cocos2d::CCNotificationCenter::sharedNotificationCenter()->postNotification("IAP_MSG");
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
}
- (void)restoreTransaction:(SKPaymentTransaction *)transaction {
    NSLog(@"已经购买过了");
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
}


@end
