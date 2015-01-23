//
//  IAPPay.h
//  sgz
//
//  Created by apple on 14/12/17.
//
//

#import <Foundation/Foundation.h>
#import <StoreKit/StoreKit.h>
#import "OC2dPlugin.h"

@interface C2dPluginIAP : OC2dPlugin <SKProductsRequestDelegate,SKPaymentTransactionObserver>

@end
