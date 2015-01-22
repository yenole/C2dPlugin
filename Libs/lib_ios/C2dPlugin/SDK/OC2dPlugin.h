//
//  OC2dPlugin.h
//  plugindemo
//
//  Created by apple on 15/1/20.
//
//

#import <Foundation/Foundation.h>

@interface OC2dPlugin : NSObject{
@public va_list __argv;
}

- (NSString*) invoke:(NSString*) funcName;

- (void) postNotification:(NSString *) notify :(NSString *) value;

- (BOOL) getBoolArgv;

- (char) getCharArgv;

- (int) getIntArgv;

- (long) getLongArgv;

- (float) getFloatArgv;

- (double) getDoubleArgv;

- (NSString *) getStringArgv;

@end
