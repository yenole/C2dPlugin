//
//  IAPPay.m
//  sgz
//
//  Created by apple on 14/12/17.
//
//

#import "C2dPluginIAP.h"

@implementation C2dPluginIAP


-(NSString *)invoke:(NSString *)funcName
{
    if ([@"init" isEqualToString:funcName]) {
        [[SKPaymentQueue defaultQueue] addTransactionObserver:self];
        return @"1";
    }
    else if ([@"buy" isEqualToString:funcName]){
        if ([SKPaymentQueue canMakePayments]) {
            
            NSArray* transactions = [SKPaymentQueue defaultQueue].transactions;
            if (transactions.count > 0) {
                //检测是否有未完成的交易
                SKPaymentTransaction* transaction = [transactions firstObject];
                if (transaction.transactionState == SKPaymentTransactionStatePurchased) {
                    [[SKPaymentQueue defaultQueue] finishTransaction:transaction];
                }
            }
            
            NSSet * set = [NSSet setWithArray:@[[self getStringArgv]]];
            SKProductsRequest * request = [[SKProductsRequest alloc] initWithProductIdentifiers:set];
            request.delegate = self;
            [request start];
            return @"1";
        }
    }
    return nil;
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
        [self postNotification:@"IAP_MSG" :@"无法获取产品信息，购买失败。"];
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
    [self postNotification:@"IAP_MSG" :transaction.transactionIdentifier];
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
    
}
- (void)failedTransaction:(SKPaymentTransaction *)transaction {
    if(transaction.error.code != SKErrorPaymentCancelled) {
        NSLog(@"购买失败");
        [self postNotification:@"IAP_MSG" :@"购买失败"];
    } else {
        NSLog(@"用户取消交易");
        [self postNotification:@"IAP_MSG" :@"用户取消交易"];
    }
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
}
- (void)restoreTransaction:(SKPaymentTransaction *)transaction {
    NSLog(@"已经购买过了");
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
}


@end
