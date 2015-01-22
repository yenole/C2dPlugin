//
//  IAPPay.h
//  sgz
//
//  Created by apple on 14/12/17.
//
//

#import <Foundation/Foundation.h>
#import <StoreKit/StoreKit.h>

@interface IAPPay : NSObject <SKProductsRequestDelegate,SKPaymentTransactionObserver>

+ (IAPPay *) ShareInstance;

- (BOOL) canMakePayments;

- (void) buyWithProduceId:(NSString *)proid;

@end
